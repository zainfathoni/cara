"""Pinned, credential-free installation and isolated upstream process state."""

import hashlib
import io
import os
from pathlib import Path
import platform
import subprocess
import tarfile
import tempfile
import urllib.request
from contextlib import contextmanager


VERSION = "4.0.1"
HOST = "https://app.fizzy.do"
ACCOUNT = "6104728"
RELEASE = f"https://github.com/basecamp/fizzy-cli/releases/download/v{VERSION}"
# Archive hashes are from the official release's checksums.txt. Binary hashes
# were derived by extracting those verified archives, without executing them.
LINUX = {
    "amd64": (
        "8a3a6b48d6eb732a189a3b18d863a1db6497a55926fd6efa4ace92e9d0a30572",
        "928ac813a7aac1f0c13db5974d6f40b16e77eda21f625ec01a49b7c365f2a9a7",
    ),
    "arm64": (
        "b96a0522929b28931a68fc11c2c5b957990d10caa831629252831631bba89dde",
        "320a3ed541ea71b15519c65cf27cac8155f0f0189a9c2fad2d317a7a0c41acc0",
    ),
}
BREW_PREFIXES = (Path("/opt/homebrew"), Path("/usr/local"))


class RuntimeErrorSafe(Exception):
    """An operator-facing error that contains no credentials or subprocess output."""


@contextmanager
def isolated_state(token=None):
    # Explicit /tmp avoids project-controlled TMPDIR. A local empty config stops
    # upstream's ancestor walk before it can reach any ambient .fizzy.yaml.
    with tempfile.TemporaryDirectory(prefix="cara-fizzy-", dir="/tmp") as temp:
        home = Path(temp)
        config = home / ".config/fizzy"
        config.mkdir(parents=True, mode=0o700)
        (home / ".fizzy.yaml").write_text("{}\n")
        # This private directory is newly created, so no shared marker/symlink
        # can be followed. Never touch the real HOME's skills or version marker.
        with (config / ".last-run-version").open("x") as marker:
            marker.write(VERSION + "\n")
        env = {
            "HOME": str(home),
            "PATH": os.defpath,
            "LANG": "C.UTF-8",
            "TMPDIR": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_STATE_HOME": str(home / ".local/state"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "FIZZY_PROFILE": ACCOUNT,
            "FIZZY_API_URL": HOST,
            "FIZZY_NO_KEYRING": "1",
            "FIZZY_NO_UPDATE_NOTIFIER": "1",
        }
        if token is not None:
            env["FIZZY_TOKEN"] = token
        yield home, env


def verify_version(binary):
    with isolated_state() as (home, env):
        try:
            result = subprocess.run(
                [str(binary), "--version"], cwd=home, env=env,
                capture_output=True, timeout=15,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise RuntimeErrorSafe("Cannot execute the pinned Fizzy binary.") from None
    if result.returncode or result.stdout.strip() != f"fizzy version {VERSION}".encode():
        raise RuntimeErrorSafe("Fizzy must be exactly 4.0.1; automatic upgrades are disabled.")


class HTTPSRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlsplit(newurl).scheme != "https":
            raise RuntimeErrorSafe("Refusing a non-HTTPS release redirect.")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_archive(arch):
    # No ambient proxies, URL overrides, curl config, or credentials.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), HTTPSRedirect())
    url = f"{RELEASE}/fizzy_{VERSION}_linux_{arch}.tar.gz"
    try:
        with opener.open(url, timeout=45) as response:
            archive = response.read(64 * 1024 * 1024 + 1)
    except (OSError, ValueError):
        raise RuntimeErrorSafe("Cannot download the official Fizzy 4.0.1 archive.") from None
    if hashlib.sha256(archive).hexdigest() != LINUX[arch][0]:
        raise RuntimeErrorSafe("Official Fizzy archive checksum mismatch; nothing installed.")
    return archive


def private_install_dir(home, arch):
    target = home / ".local/share/cara/fizzy" / VERSION / ("linux_" + arch)
    # Resolve HOME itself (macOS commonly aliases home paths), but reject
    # symlinks in every installer-owned path before writing or replacing files.
    path = home
    for part in target.relative_to(home).parts:
        path = path / part
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise RuntimeErrorSafe("Refusing a symlink or non-directory in the Fizzy install path.")
    return target


def ensure_binary(check=False):
    system, machine = platform.system(), platform.machine().lower()
    if system == "Darwin":
        # Read the package-managed executable directly. Do not invoke PATH's
        # fizzy wrapper, brew itself, or modify a Homebrew file or symlink.
        for prefix in BREW_PREFIXES:
            prefix = prefix.resolve()
            candidate = prefix / "bin/fizzy"
            if not candidate.exists():
                continue
            binary = candidate.resolve()
            if not any(root in binary.parents for root in
                       (prefix / "Caskroom/fizzy", prefix / "Cellar/fizzy")):
                continue
            verify_version(binary)
            return binary
        raise RuntimeErrorSafe("An existing direct Homebrew Fizzy 4.0.1 binary is required on macOS.")
    if system != "Linux" or machine not in ("x86_64", "amd64", "aarch64", "arm64"):
        raise RuntimeErrorSafe("Supported platforms: Linux x64/arm64 and macOS with Homebrew Fizzy 4.0.1.")
    arch = "amd64" if machine in ("x86_64", "amd64") else "arm64"
    directory = private_install_dir(Path.home().resolve(), arch)
    binary = directory / "fizzy"
    if binary.is_symlink():
        raise RuntimeErrorSafe("Refusing a symlinked Fizzy executable.")
    if binary.is_file() and hashlib.sha256(binary.read_bytes()).hexdigest() == LINUX[arch][1]:
        verify_version(binary)
        return binary
    if check:
        raise RuntimeErrorSafe("Verified Fizzy 4.0.1 is missing; run install_fizzy.py or the scoped runner.")
    archive = download_archive(arch)
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
            members = [entry for entry in tar.getmembers() if entry.name == "fizzy"]
            if len(members) != 1 or not members[0].isfile() or members[0].size > 128 * 1024 * 1024:
                raise RuntimeErrorSafe("Invalid executable in the verified Fizzy archive.")
            payload = tar.extractfile(members[0]).read()
    except (tarfile.TarError, OSError):
        raise RuntimeErrorSafe("Cannot unpack the verified Fizzy archive.") from None
    if hashlib.sha256(payload).hexdigest() != LINUX[arch][1]:
        raise RuntimeErrorSafe("Fizzy executable checksum mismatch; nothing installed.")
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.TemporaryDirectory(prefix=".install-", dir=directory) as temp:
        staged = Path(temp) / "fizzy"
        staged.write_bytes(payload)
        staged.chmod(0o755)
        verify_version(staged)
        os.replace(staged, binary)
    return binary
