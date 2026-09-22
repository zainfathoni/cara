"""Bounded routing, installation integrity, and real-CLI loopback checks.

No live API calls or credentials. Optional CARA_FIZZY_TEST_BINARY selects an
existing 4.0.1 executable; the direct Homebrew executable is detected on macOS.
"""

import contextlib
import hashlib
import http.server
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parents[2] / "skills/fizzy/scripts"
sys.path.insert(0, str(SCRIPTS))
import fizzy_amp as amp
import fizzy_runtime as runtime

WORK = "03fj2n6bhaen2sq6jb9zs1eon"
PERSONAL = "03fipgbrb5fhrokehz4plyjha"
RED_ALERT = "03fj2nej4tfeyw5paunpl06i3"
WHEELJACK = "03fipgbrb5fhrokehz4plyjht"
CHILD = "03fipgbrb5fhrokehz4plyjhb"


def ok(data):
    return {"ok": True, "data": data}


class FakeRunner(amp.Runner):
    def __init__(self, scope="work", board=WORK, user=None, slug="/6104728"):
        super().__init__(Path("/unused"), Path("/unused"), {}, scope)
        self.calls = []
        self.card_board, self.slug = board, slug
        self.user = user or (RED_ALERT if scope == "work" else WHEELJACK)
        self.number = 579
        self.columns = [{"id": CHILD}]

    def call(self, args):
        self.calls.append(args)
        if args[:2] == ["identity", "show"]:
            return ok({"accounts": [{"slug": self.slug, "user": {"id": self.user}}]})
        if args[:2] == ["card", "show"]:
            return ok({"number": self.number, "board": {"id": self.card_board}})
        if args[:2] == ["board", "show"]:
            return ok({"id": args[2]})
        if args[:2] == ["column", "list"]:
            return ok(self.columns)
        if args[:2] == ["board", "list"]:
            return ok([{"id": WORK}, {"id": PERSONAL}])
        if args[0] == "search":
            return ok([{"number": 579, "board": {"id": WORK}},
                       {"number": 580, "board": {"id": PERSONAL}}])
        return ok({})

    def run(self, *args):
        return self.execute(*amp.parse_operation(list(args)))


class RoutingTests(unittest.TestCase):
    def test_live_identity_slug_forms_and_corrected_actor(self):
        for scope, user in (("work", RED_ALERT), ("personal", WHEELJACK)):
            for slug in ("6104728", "/6104728"):
                with self.subTest(scope=scope, slug=slug):
                    data = FakeRunner(scope, user=user, slug=slug).identity()["data"]
                    self.assertEqual(data["accounts"][0]["user"]["id"], user)
        for slug in ("//6104728", "6104728/", "/6104728/", "/9999999", 6104728):
            with self.subTest(slug=slug), self.assertRaises(runtime.RuntimeErrorSafe):
                FakeRunner(slug=slug).identity()

    def test_stale_or_wrong_actor_blocks_before_mutation(self):
        for user in ("03fj2j4swdfvhq6a6rj0f4n6h", WHEELJACK):
            runner = FakeRunner(user=user)
            with self.assertRaises(runtime.RuntimeErrorSafe):
                runner.run("card", "close", "579")
            self.assertEqual(runner.calls, [["identity", "show"]])

    def test_card_number_is_resolved_before_mutation(self):
        runner = FakeRunner()
        runner.run("card", "update", "579", "--title=Reviewed")
        self.assertEqual(runner.calls, [
            ["identity", "show"], ["card", "show", "579"],
            ["card", "update", "579", "--title=Reviewed"],
        ])

    def test_wrong_board_and_mismatched_lookup_never_mutate(self):
        for scope, board in (("work", PERSONAL), ("personal", WORK)):
            runner = FakeRunner(scope, board)
            with self.assertRaises(runtime.RuntimeErrorSafe):
                runner.run("comment", "create", "--card", "579", "--body", "hello")
            self.assertEqual(len(runner.calls), 2)
        runner = FakeRunner()
        runner.number = 580
        with self.assertRaises(runtime.RuntimeErrorSafe):
            runner.run("card", "close", "579")
        self.assertEqual(len(runner.calls), 2)

    def test_board_create_update_and_cross_scope_move(self):
        runner = FakeRunner()
        runner.run("card", "create", "--title", "From any Amp project")
        self.assertEqual(runner.calls[1], ["board", "show", WORK])
        self.assertIn("--board=" + WORK, runner.calls[-1])
        runner = FakeRunner("personal", PERSONAL)
        runner.run("board", "update", PERSONAL, "--name", "Projects")
        self.assertEqual(runner.calls[1], ["board", "show", PERSONAL])
        for scope, target in (("work", PERSONAL), ("personal", WORK)):
            runner = FakeRunner(scope)
            with self.assertRaises(runtime.RuntimeErrorSafe):
                runner.run("card", "move", "579", "--to", target)
            self.assertEqual(runner.calls, [])
        with self.assertRaises(runtime.RuntimeErrorSafe):
            FakeRunner().run("board", "create", "--name", "Work copy")
        runner = FakeRunner("personal", PERSONAL)
        runner.run("board", "create", "--name", "Another board")
        self.assertEqual(runner.calls[-1], ["board", "create", "--name=Another board"])

    def test_personal_board_requests_need_an_explicit_target(self):
        for command in (("card", "list"), ("card", "create", "--title", "x"),
                        ("activity", "list"), ("column", "list")):
            runner = FakeRunner("personal", PERSONAL)
            with self.subTest(command=command), self.assertRaises(runtime.RuntimeErrorSafe):
                runner.run(*command)
            self.assertEqual(runner.calls, [])

    def test_discovery_filters_to_selected_scope(self):
        for scope, board in (("work", WORK), ("personal", PERSONAL)):
            runner = FakeRunner(scope)
            self.assertEqual(runner.run("board", "list", "--all")["data"], [{"id": board}])
            self.assertEqual(runner.run("search", "query")["data"][0]["board"]["id"], board)

    def test_column_must_belong_to_card_board(self):
        runner = FakeRunner()
        runner.run("card", "column", "579", "--column", CHILD)
        self.assertEqual(runner.calls[-2], ["column", "list", "--board=" + WORK])
        runner = FakeRunner()
        runner.columns = []
        with self.assertRaises(runtime.RuntimeErrorSafe):
            runner.run("card", "column", "579", "--column", CHILD)
        self.assertEqual(runner.calls[-1][:2], ["column", "list"])

    def test_steps_status_and_markdown_keep_one_card_target(self):
        commands = [
            ("comment", "create", "--card", "579", "--body", "**Review**\n\n- one"),
            ("step", "create", "--card", "579", "--content", "Review"),
            ("step", "update", CHILD, "--card", "579", "--completed"),
            ("step", "update", CHILD, "--card", "579", "--not_completed"),
            ("card", "close", "579"), ("card", "reopen", "579"),
            ("card", "postpone", "579"), ("card", "column", "579", "--column", "done"),
        ]
        for args in commands:
            with self.subTest(args=args):
                runner = FakeRunner()
                runner.run(*args)
                self.assertEqual(runner.calls[1], ["card", "show", "579"])
                self.assertEqual(len(runner.calls), 3)

    def test_unsupported_shapes_overrides_and_query_injection_fail_closed(self):
        commands = [
            ["card", "close", "579", "580"], ["card", "close", WORK],
            ["card", "close", "579/../580"], ["card", "delete", "579"],
            ["auth", "login", "dummy"], ["config", "show"], ["migrate", "board"],
            ["card", "create", "--title", "x", "--attach", "file"],
            ["card", "list", "--board", WORK + "&board_ids[]=" + PERSONAL],
            ["card", "list", "--search", "x&board_ids[]=other"],
            ["card", "list", "--search", "%26board_ids"],
            ["card", "list", "--board", WORK, "--board", PERSONAL],
            ["card", "show", "579", "--json=false"],
            ["card", "move", "579", "-t", PERSONAL],
        ]
        for flag in ("--token=dummy", "--profile=other", "--api-url=http://host",
                     "--verbose", "--agent", "--jq=.data", "--help", "--", "-h"):
            commands.append(["card", "close", "579", flag])
        for args in commands:
            with self.subTest(args=args), self.assertRaises(runtime.RuntimeErrorSafe):
                amp.parse_operation(args)

    def test_markdown_file_is_absolute_before_changing_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            original = Path.cwd()
            try:
                os.chdir(temp)
                Path("body.md").write_text("# Heading\n\n**Bold**")
                _, _, flags = amp.parse_operation(["card", "update", "579", "--description_file", "body.md"])
            finally:
                os.chdir(original)
            self.assertEqual(flags["description_file"], str(Path(temp).resolve() / "body.md"))

    def test_no_scope_or_missing_secret_never_installs_or_falls_back(self):
        with patch.dict(os.environ, {"FIZZY_TOKEN": "ambient"}, clear=True), \
                patch.object(amp, "ensure_binary") as install, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(amp.main(["card", "show", "579"]), 1)
            self.assertEqual(amp.main(["--scope", "personal", "card", "show", "579"]), 1)
            install.assert_not_called()

    def test_only_selected_secret_reaches_process_and_is_not_saved(self):
        with tempfile.TemporaryDirectory() as temp:
            real_home = Path(temp)
            (real_home / ".fizzy.yaml").write_text("token: saved-fixture\n")
            dirty = {"HOME": temp, "FIZZY_TOKEN": "ambient", "FIZZY_PROFILE": "other",
                     "FIZZY_API_URL": "http://other", "FIZZY_BOARD": PERSONAL,
                     "FIZZY_DEBUG": "1", "HTTPS_PROXY": "http://other",
                     "FIZZY_WHEELJACK_TOKEN": "other-secret", "AMP_TOKEN": "unrelated"}
            with patch.dict(os.environ, dirty), runtime.isolated_state("selected-fixture") as (home, env):
                self.assertEqual(env["FIZZY_TOKEN"], "selected-fixture")
                self.assertEqual(env["FIZZY_PROFILE"], "6104728")
                self.assertEqual(env["FIZZY_API_URL"], "https://app.fizzy.do")
                for key in dirty:
                    if key not in ("HOME", "FIZZY_TOKEN", "FIZZY_PROFILE", "FIZZY_API_URL"):
                        self.assertNotIn(key, env)
                self.assertEqual((home / ".config/fizzy/.last-run-version").read_text().strip(), "4.0.1")
                for path in home.rglob("*"):
                    if path.is_file():
                        self.assertNotIn(b"selected-fixture", path.read_bytes())
            self.assertFalse(home.exists())
            self.assertEqual((real_home / ".fizzy.yaml").read_text(), "token: saved-fixture\n")

    def test_failure_and_timeout_do_not_echo_upstream_secret(self):
        runner = amp.Runner(Path("/unused"), Path("/unused"), {}, "work")
        result = subprocess.CompletedProcess([], 1, b'{"ok":false,"code":"AUTH","error":"synthetic-secret"}', b"synthetic-secret")
        with patch.object(amp.subprocess, "run", return_value=result):
            with self.assertRaises(runtime.RuntimeErrorSafe) as error:
                runner.call(["card", "close", "579"])
            self.assertNotIn("synthetic-secret", str(error.exception))
            self.assertIn("AUTH", str(error.exception))
        with patch.object(amp.subprocess, "run", side_effect=subprocess.TimeoutExpired([], 120)):
            with self.assertRaisesRegex(runtime.RuntimeErrorSafe, "outcome may be unknown"):
                runner.call(["card", "close", "579"])


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        for name, value in (("system", "Linux"), ("machine", "x86_64")):
            mock = patch.object(runtime.platform, name, return_value=value)
            mock.start()
            self.addCleanup(mock.stop)
        mock = patch.object(runtime.Path, "home", return_value=self.home)
        mock.start()
        self.addCleanup(mock.stop)

    def fixture(self, arch):
        payload = b'#!/bin/sh\necho "fizzy version 4.0.1"\n'
        archive = io.BytesIO()
        with tarfile.open(fileobj=archive, mode="w:gz") as tar:
            item = tarfile.TarInfo("fizzy")
            item.size = len(payload)
            tar.addfile(item, io.BytesIO(payload))
        data = archive.getvalue()
        pins = (hashlib.sha256(data).hexdigest(), hashlib.sha256(payload).hexdigest())
        return data, payload, pins

    def test_both_architectures_install_verify_and_reuse_without_download(self):
        for machine, arch in (("x86_64", "amd64"), ("aarch64", "arm64")):
            data, payload, pins = self.fixture(arch)
            with patch.object(runtime.platform, "machine", return_value=machine), \
                    patch.dict(runtime.LINUX, {arch: pins}), \
                    patch.object(runtime, "download_archive", return_value=data) as download:
                binary = runtime.ensure_binary()
                self.assertEqual(binary.read_bytes(), payload)
                self.assertEqual(runtime.ensure_binary(check=True), binary)
                self.assertEqual(runtime.ensure_binary(), binary)
                download.assert_called_once_with(arch)

    def test_check_never_downloads_and_corrupt_archive_preserves_binary(self):
        with patch.object(runtime, "download_archive") as download:
            with self.assertRaises(runtime.RuntimeErrorSafe):
                runtime.ensure_binary(check=True)
            download.assert_not_called()
        directory = runtime.private_install_dir(self.home, "amd64")
        directory.mkdir(parents=True)
        binary = directory / "fizzy"
        binary.write_bytes(b"preserve previous binary")
        response = io.BytesIO(b"corrupt archive")
        with patch.object(runtime.urllib.request.OpenerDirector, "open", return_value=response):
            with self.assertRaisesRegex(runtime.RuntimeErrorSafe, "checksum mismatch"):
                runtime.ensure_binary()
        self.assertEqual(binary.read_bytes(), b"preserve previous binary")

    def test_symlink_ancestors_and_binary_are_rejected(self):
        (self.home / ".local").symlink_to(self.home / "elsewhere")
        with self.assertRaises(runtime.RuntimeErrorSafe):
            runtime.ensure_binary()
        (self.home / ".local").unlink()
        directory = runtime.private_install_dir(self.home, "amd64")
        directory.mkdir(parents=True)
        (directory / "fizzy").symlink_to(self.home / "elsewhere")
        with self.assertRaises(runtime.RuntimeErrorSafe):
            runtime.ensure_binary()

    def test_mac_direct_homebrew_binary_is_preserved(self):
        binary = self.home / "Caskroom/fizzy/4.0.1/fizzy"
        binary.parent.mkdir(parents=True)
        binary.write_text('#!/bin/sh\necho "fizzy version 4.0.1"\n')
        binary.chmod(0o755)
        (self.home / "bin").mkdir()
        link = self.home / "bin/fizzy"
        link.symlink_to(binary)
        before = binary.stat()
        with patch.object(runtime.platform, "system", return_value="Darwin"), \
                patch.object(runtime, "BREW_PREFIXES", (self.home,)), \
                patch.object(runtime, "download_archive") as download:
            self.assertEqual(runtime.ensure_binary(), binary.resolve())
            self.assertEqual(runtime.ensure_binary(check=True), binary.resolve())
            download.assert_not_called()
        self.assertTrue(link.is_symlink())
        self.assertEqual(binary.stat().st_mtime_ns, before.st_mtime_ns)
        self.assertEqual(binary.stat().st_ino, before.st_ino)

    def test_unsupported_os_and_https_downgrade_rejected(self):
        with patch.object(runtime.platform, "system", return_value="Windows"):
            with self.assertRaises(runtime.RuntimeErrorSafe):
                runtime.ensure_binary()
        with self.assertRaises(runtime.RuntimeErrorSafe):
            runtime.HTTPSRedirect().redirect_request(None, None, 302, "", {}, "http://host/binary")


REAL_BINARY = os.environ.get("CARA_FIZZY_TEST_BINARY")
if not REAL_BINARY and sys.platform == "darwin":
    candidate = Path("/opt/homebrew/Caskroom/fizzy/4.0.1/fizzy")
    if candidate.is_file():
        REAL_BINARY = str(candidate)


@unittest.skipUnless(REAL_BINARY, "No existing upstream binary for loopback integration")
class UpstreamTests(unittest.TestCase):
    def test_real_cli_identity_routing_markdown_and_skill_preservation(self):
        requests = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def handle_request(handler):
                body = handler.rfile.read(int(handler.headers.get("Content-Length", 0)))
                requests.append((handler.command, handler.path,
                                 handler.headers.get("Authorization"), body))
                if handler.path == "/my/identity.json":
                    data = {"accounts": [{"slug": "/6104728", "user": {"id": RED_ALERT, "active": True}}]}
                elif handler.path.endswith("/boards/" + WORK + ".json"):
                    data = {"id": WORK}
                else:
                    data = {"number": 579, "board": {"id": WORK}, "id": CHILD}
                handler.send_response(200)
                handler.send_header("Content-Type", "application/json")
                handler.end_headers()
                handler.wfile.write(json.dumps(data).encode())

            do_GET = handle_request
            do_POST = handle_request
            do_PUT = handle_request
            do_PATCH = handle_request

            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        url = f"http://127.0.0.1:{server.server_port}"
        runtime.verify_version(Path(REAL_BINARY))
        with runtime.isolated_state("synthetic-loopback-token") as (home, env):
            custom = home / "custom/SKILL.md"
            custom.parent.mkdir()
            custom.write_text("Preserve this customized hosted skill.\n")
            skill = home / ".agents/skills/fizzy"
            skill.parent.mkdir(parents=True)
            skill.symlink_to(custom.parent)
            env["FIZZY_API_URL"] = url
            # Test-only in-memory patch, no production endpoint/binary override.
            with patch.object(amp, "HOST", url):
                runner = amp.Runner(Path(REAL_BINARY), home, env, "work")
                runner.execute(*amp.parse_operation(["card", "create", "--title", "fixture",
                                                     "--description", "**Bold**\n\n- item"]))
                runner.execute(*amp.parse_operation(["comment", "create", "--card", "579",
                                                     "--body", "**Comment**"]))
                runner.execute(*amp.parse_operation(["step", "update", CHILD, "--card", "579", "--completed"]))
                runner.execute(*amp.parse_operation(["card", "close", "579"]))
            self.assertTrue(skill.is_symlink())
            self.assertEqual(custom.read_text(), "Preserve this customized hosted skill.\n")
            for path in home.rglob("*"):
                if path.is_file():
                    self.assertNotIn(b"synthetic-loopback-token", path.read_bytes())
            self.assertFalse((home / ".config/fizzy/credentials").exists())
        for method, path, auth, body in requests:
            self.assertEqual(auth, "Bearer synthetic-loopback-token")
            self.assertTrue(path == "/my/identity.json" or path.startswith("/6104728/"))
        writes = [(method, path, json.loads(body) if body else {})
                  for method, path, auth, body in requests if method != "GET"]
        self.assertEqual(len(writes), 4)
        self.assertIn("<strong>Bold</strong>", json.dumps(writes[0][2]))
        self.assertIn("<strong>Comment</strong>", json.dumps(writes[1][2]))
        self.assertIn("/cards/579/", writes[1][1])
        self.assertIn("/cards/579/steps/", writes[2][1])
        self.assertIn("/cards/579/", writes[3][1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
