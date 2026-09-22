#!/usr/bin/env python3
"""Run bounded Fizzy operations with --scope work|personal, from any project.

Usage: python3 fizzy_amp.py --scope work card show 579 --json
See README.md beside this script for the supported commands and flags.
"""

import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
from fizzy_runtime import ACCOUNT, HOST, RuntimeErrorSafe, ensure_binary, isolated_state


WORK_BOARD = "03fj2n6bhaen2sq6jb9zs1eon"
SCOPES = {
    "work": ("FIZZY_REDALERT_TOKEN", "03fj2nej4tfeyw5paunpl06i3"),
    "personal": ("FIZZY_WHEELJACK_TOKEN", "03fipgbrb5fhrokehz4plyjht"),
}
ID = re.compile(r"[a-z0-9]{20,32}\Z")
NUMBER = re.compile(r"[1-9][0-9]*\Z")

# Each entry is (positional count, value flags, boolean flags). This is a small
# policy surface, not a general Cobra parser. Only canonical long flags pass.
PAGE = "page"
RICH_CARD = "title description description_file"
RICH_COMMENT = "card body body_file"
OPS = {
    "identity show": (0, "", ""),
    "account show": (0, "", ""),
    "user list": (0, PAGE, "all"),
    "user show": (1, "", ""),
    "tag list": (0, PAGE, "all"),
    "board list": (0, PAGE, "all"),
    "board show": (1, "", ""),
    "board create": (0, "name all_access auto_postpone_period_in_days", ""),
    "board update": (1, "name all_access auto_postpone_period_in_days", ""),
    "board accesses": (0, "board page", ""),
    "board closed": (0, "board page", "all"),
    "board postponed": (0, "board page", "all"),
    "board stream": (0, "board page", "all"),
    "column list": (0, "board", ""),
    "column show": (1, "board", ""),
    "column create": (0, "board name color", ""),
    "column update": (1, "board name color", ""),
    "activity list": (0, "board creator page", "all"),
    "card list": (0, "board column tag indexed-by status assignee search sort creator closer created closed page", "all unassigned"),
    "card show": (1, "", ""),
    "card create": (0, "board " + RICH_CARD, ""),
    "card update": (1, RICH_CARD, ""),
    "card move": (1, "to", ""),
    "card column": (1, "column", ""),
    "card assign": (1, "user", ""),
    "card tag": (1, "tag", ""),
    "comment list": (0, "card page", "all"),
    "comment show": (1, "card", ""),
    "comment create": (0, RICH_COMMENT, ""),
    "comment update": (1, RICH_COMMENT, ""),
    "step list": (0, "card", ""),
    "step show": (1, "card", ""),
    "step create": (0, "card content", "completed"),
    "step update": (1, "card content", "completed not_completed"),
    "search": (1, "", ""),
}
for action in ("close reopen postpone untriage self-assign watch unwatch pin unpin "
               "golden ungolden publish mark-read mark-unread").split():
    OPS["card " + action] = (1, "", "")


def reject(message):
    raise RuntimeErrorSafe(message)


def identifier(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        reject("Expected a Fizzy resource ID, with no URL, path, or query syntax.")
    return value


def card_number(value):
    if not isinstance(value, str) or not NUMBER.fullmatch(value):
        reject("Use a positive card number; resolve card IDs with a scoped search first.")
    return value


def parse_operation(argv):
    if not argv:
        reject("A supported Fizzy operation is required; see scripts/README.md.")
    count = 1 if argv[0] == "search" else 2
    op = " ".join(argv[:count])
    if op not in OPS:
        reject("Unsupported operation; see scripts/README.md for the bounded command list.")
    arity, values, booleans = OPS[op]
    values, booleans = set(values.split()), set(booleans.split()) | {"json"}
    positional, flags = [], {}
    tail = iter(argv[count:])
    for arg in tail:
        if not arg.startswith("-"):
            positional.append(arg)
            continue
        name, equal, value = arg.removeprefix("--").partition("=")
        if not arg.startswith("--") or name not in values | booleans:
            reject("Unsupported flag; credentials, profiles, hosts, debug, and output overrides are forbidden.")
        if name in flags:
            reject("Repeated flags are unsupported; split requests into one target and scope per invocation.")
        if name in booleans:
            value = value if equal else "true"
            if value not in ("true", "false") or (name == "json" and value != "true"):
                reject("Boolean flags accept only true/false; JSON output cannot be disabled.")
        elif not equal:
            value = next(tail, None)
            if value is None or value.startswith("--"):
                reject("A flag value is missing; use --name=value for text starting with --.")
        flags[name] = value
    if len(positional) != arity:
        reject("Unexpected arguments; use one target (or one quoted search query) per invocation.")
    flags.pop("json", None)
    if op.startswith("card ") and arity:
        card_number(positional[0])
    elif arity and op != "search":
        identifier(positional[0])
    for name in ("board", "to", "user", "assignee", "creator", "closer"):
        if name in flags:
            identifier(flags[name])
    if "card" in flags:
        card_number(flags["card"])
    if "column" in flags and flags["column"] not in ("not-now", "maybe", "done"):
        identifier(flags["column"])
    if "page" in flags and not NUMBER.fullmatch(flags["page"]):
        reject("--page must be a positive integer.")
    # Upstream's raw card-list query builder concatenates some values without
    # encoding. Reject query delimiters even in search/filter text.
    if op == "card list" and any(any(c in v for c in "&#%?\r\n") for v in flags.values()):
        reject("Card-list filters cannot contain URL query delimiters; use scoped search for free text.")
    for inline, filename in (("description", "description_file"), ("body", "body_file")):
        if inline in flags and filename in flags:
            reject("Use either inline text or a file, not both.")
        if filename in flags:
            path = Path(flags[filename]).expanduser().resolve()
            if not path.is_file():
                reject("The requested Markdown/HTML input file is not a regular file.")
            flags[filename] = str(path)
    if flags.get("completed") == flags.get("not_completed") == "true":
        reject("Choose completed or not_completed, not both.")
    required = {
        "board create": ("name",), "column create": ("name",),
        "card create": ("title",), "card move": ("to",),
        "card column": ("column",), "card assign": ("user",),
        "card tag": ("tag",), "step create": ("content",),
    }
    if any(not flags.get(name) for name in required.get(op, ())):
        reject("A required operation flag is missing; see scripts/README.md.")
    if op in ("comment create", "comment update") and not any(flags.get(f) for f in ("body", "body_file")):
        reject("Comment create/update requires --body or --body_file.")
    return op, positional, flags


def board_in_scope(scope, board):
    identifier(board)
    return (board == WORK_BOARD) == (scope == "work")


def require_scope(scope, board):
    if not board_in_scope(scope, board):
        reject("Board does not match --scope; split Work and other-board requests by scope.")


class Runner:
    def __init__(self, binary, home, env, scope):
        self.binary, self.home, self.env, self.scope = binary, home, env, scope

    def call(self, args):
        command = [str(self.binary), *args, "--json", "--profile=" + ACCOUNT, "--api-url=" + HOST]
        try:
            result = subprocess.run(command, env=self.env, cwd=self.home,
                                    capture_output=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired):
            reject("Fizzy process failed or timed out; mutation outcome may be unknown. Read back before retrying.")
        try:
            envelope = json.loads(result.stdout)
        except (ValueError, UnicodeError):
            reject("Fizzy returned an invalid JSON response; read back before retrying a mutation.")
        if not isinstance(envelope, dict) or result.returncode or envelope.get("ok") is not True:
            code = envelope.get("code", "UNKNOWN") if isinstance(envelope, dict) else "UNKNOWN"
            # Do not echo subprocess error text, which may include request data.
            if not isinstance(code, str) or not re.fullmatch(r"[A-Z_]{1,40}", code):
                code = "UNKNOWN"
            reject(f"Fizzy request failed ({code}); no further operation was run. Read back before retrying a mutation.")
        return envelope

    def identity(self):
        envelope = self.call(["identity", "show"])
        data = envelope.get("data")
        accounts = data.get("accounts") if isinstance(data, dict) else None
        if not isinstance(accounts, list):
            reject("Identity response has no account list.")
        selected = [a for a in accounts if isinstance(a, dict) and
                    a.get("slug") in (ACCOUNT, "/" + ACCOUNT)]
        if len(selected) != 1 or not isinstance(selected[0].get("user"), dict):
            reject("Identity did not uniquely resolve account 6104728.")
        user = selected[0]["user"]
        if user.get("id") != SCOPES[self.scope][1] or user.get("active") is False:
            reject("Acting user does not match the selected scope; check user-level secret provisioning.")
        envelope["data"] = {"accounts": selected}
        return envelope

    def board(self, board):
        require_scope(self.scope, board)
        data = self.call(["board", "show", board]).get("data")
        if not isinstance(data, dict) or data.get("id") != board:
            reject("Board lookup did not return the requested board ID.")

    def card(self, number):
        envelope = self.call(["card", "show", card_number(number)])
        data = envelope.get("data")
        if not isinstance(data, dict) or str(data.get("number")) != number:
            reject("Card lookup did not return the requested card number.")
        board = data.get("board")
        if not isinstance(board, dict):
            reject("Card lookup has no board relationship; routing cannot be verified.")
        require_scope(self.scope, board.get("id"))
        return envelope

    def execute(self, op, positional, flags):
        # Reject known scope mismatches before even making the identity request.
        for name in ("board", "to"):
            if name in flags:
                require_scope(self.scope, flags[name])
        if op in ("board show", "board update"):
            require_scope(self.scope, positional[0])
        if op == "board create" and self.scope != "personal":
            reject("New boards belong to personal scope; work is the single pinned Work board.")
        board_required = (op in ("card list", "card create", "activity list") or
                          op.startswith("column ") or
                          op in ("board accesses", "board closed", "board postponed", "board stream"))
        if board_required and "board" not in flags:
            if self.scope == "work":
                flags["board"] = WORK_BOARD
            else:
                reject("Personal board-targeted operations require one explicit --board ID.")
        if op.startswith(("comment ", "step ")) and "card" not in flags:
            reject("Comment and step operations require an explicit --card NUMBER.")
        identity = self.identity()
        if op == "identity show":
            return identity
        if "board" in flags:
            self.board(flags["board"])
        if "to" in flags:
            self.board(flags["to"])
        if op in ("board show", "board update"):
            self.board(positional[0])
        number = positional[0] if op.startswith("card ") and positional else flags.get("card")
        if number:
            card = self.card(number)
            if op == "card show":
                return card
            if op == "card column" and flags["column"] not in ("not-now", "maybe", "done"):
                board = card["data"]["board"]["id"]
                columns = self.call(["column", "list", "--board=" + board]).get("data")
                if not isinstance(columns, list) or not any(
                    isinstance(c, dict) and c.get("id") == flags["column"] for c in columns
                ):
                    reject("Destination column is not in the card's board.")
        args = op.split() + positional + [f"--{name}={value}" for name, value in flags.items()]
        envelope = self.call(args)
        if op in ("board list", "search"):
            items = envelope.get("data")
            if not isinstance(items, list):
                reject("Discovery response is not a list; scope filtering failed closed.")
            selected = []
            for item in items:
                if not isinstance(item, dict):
                    reject("Discovery response contains an invalid resource.")
                relationship = item.get("board")
                board = item.get("id") if op == "board list" else (
                    relationship.get("id") if isinstance(relationship, dict) else None)
                if board_in_scope(self.scope, board):
                    selected.append(item)
            envelope["data"] = selected
            envelope["summary"] = f"{len(selected)} {self.scope} results in this response"
            envelope.pop("breadcrumbs", None)
        return envelope


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv in (["--help"], ["-h"]):
        print(__doc__)
        return 0
    try:
        if len(argv) < 3 or argv[0] != "--scope" or argv[1] not in SCOPES:
            reject("Start with --scope work or --scope personal. Split mixed requests into separate invocations.")
        scope = argv[1]
        op, positional, flags = parse_operation(argv[2:])
        token_name = SCOPES[scope][0]
        token = os.environ.get(token_name)
        if not token or not token.strip():
            reject(f"Missing runtime-only {token_name}; saved credentials and ambient FIZZY_TOKEN are never used.")
        binary = ensure_binary()
        with isolated_state(token) as (home, env):
            envelope = Runner(binary, home, env, scope).execute(op, positional, flags)
        rendered = json.dumps(envelope, ensure_ascii=False)
        # Upstream diagnostics are never forwarded. Also redact credential
        # values if returned in unexpected API content; never put them in argv.
        for name, _ in SCOPES.values():
            secret = os.environ.get(name)
            if secret:
                rendered = rendered.replace(json.dumps(secret, ensure_ascii=False)[1:-1], "[REDACTED]")
        print(rendered)
        return 0
    except RuntimeErrorSafe as error:
        print(json.dumps({"ok": False, "code": "SCOPED_RUNTIME", "error": str(error)}), file=sys.stderr)
        return 1
    except OSError:
        print('{"ok":false,"code":"SCOPED_RUNTIME","error":"Cannot access the local Fizzy runtime."}', file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
