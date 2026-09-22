> Superseded: this was a project-local prototype. The owner requires Amp-wide personal skills and user-level secrets, with Red Alert on Work and Wheeljack elsewhere. The Amux hooks have been removed; shared implementation belongs to Cara.

# Fizzy access in Amp Orbs

Status: repository implementation complete; all seven focused tests pass, including real CLI account routing and skill preservation. Live Orb authentication and hosted skill publication remain owner/parent follow-up.

The Orb hooks now provide pinned Fizzy 4.0.1 alongside Go and tmux, with credentials supplied at runtime through Amp secrets and no login state written into shared snapshots. Parent-owned macOS binaries, wrapper, Cara skill and credentials were not changed.

## Findings

- Amp-hosted personal/workspace skills travel across machines and Orbs; machine-local skill installation alone does not provide that distribution. Publishing hosted skills is outside this task. See [global plugins and skills](https://ampcode.com/news/global-plugins-and-skills) and [the current workflow](https://ampcode.com/docs/customize/global-plugins-and-skills).
- Setup can be snapshotted for other project members; runtime identity belongs after activation. See [Orb lifecycle](https://ampcode.com/docs/orbs/customizing).
- Amp secrets support personal, project and workspace scopes, with personal overriding project and project overriding workspace. Each agent must receive its own intended Fizzy identity. See [handling secrets](https://ampcode.com/docs/orbs/handling-secrets).
- Fizzy 4.0.1 is published by `basecamp/fizzy-cli`. `FIZZY_ACCOUNT` is a deprecated profile alias. An isolated test with the real 4.0.1 CLI confirms that `FIZZY_TOKEN` plus `FIZZY_PROFILE=123456` works with an empty profile store: `board list` sends a GET to `/123456/boards.json` with the supplied synthetic bearer token. A persona name such as `cara` instead routes to account `cara`; it does not establish Cara's identity. Use the intended account slug as the profile in fresh Orbs.
- Source confirms that `PersistentPostRun` refreshes global skill files, following symlinks, when the version marker differs. The helper seeds the non-secret marker after checking `--version`, which bypasses config loading and the post-run hook. A real CLI fixture preserves a symlinked custom skill through successful config and board commands. No auth login or credential files are needed.

## Changed files

| File | Change |
| --- | --- |
| `.agents/setup` | Calls the pinned Fizzy installer before downloading Go dependencies. |
| `.agents/resume` | Checks the pin and reapplies the version marker before the agent starts; no download or API call. |
| `scripts/setup-fizzy-orb.sh` | Linux amd64/arm64 installation with hardcoded release SHA-256 digests, idempotent version check, and skill refresh suppression. Rejects macOS, unexpected versions in check mode, and symlinked replacement/state targets. |
| `scripts/fizzy_orb_test.py` | Temporary-home tests; optional real CLI loopback probe with synthetic credentials. |
| `README.md` | Links this setup guide. |
| `docs/fizzy-orbs-report.md` | Durable parent handoff and operator procedure. |

The helper writes only the Orb binary and a version marker. It does not install skills, save tokens, configure accounts, invoke an agent, or alter runners. The marker is a version-specific mitigation, not a supported upstream opt-out: recheck upstream refresh behavior when changing the pin. Explicit `fizzy skill` commands can still change skills.

## Owner provisioning and activation

1. Choose the exact Amp project and acting Fizzy agent. Obtain a token for that agent's own Fizzy user through the owner's trusted secret-management workflow. Do not reuse the human's or another agent's token. Record the expected account slug and that agent's user ID for the identity comparison below.
2. In that project's Amp settings, save **`FIZZY_TOKEN` as a secret**. Save **`FIZZY_PROFILE` as an environment variable containing the intended account slug** (for example, `123456`, not a persona name). `FIZZY_API_URL` may hold the intended HTTPS origin for a self-hosted instance; the CLI defaults to `https://app.fizzy.do`. Set `FIZZY_NO_UPDATE_NOTIFIER=1` as non-secret configuration to suppress unrelated update checks. Do not use the deprecated `FIZZY_ACCOUNT` alias.
3. Confirm that personal entries with these names do not override the intended project identity. Project scope applies to all Orbs in that project, so a project using this standard must have one intended Fizzy agent identity. Use separate projects or separately scoped Amp users for distinct agents; a single shared token plus different profile labels does not preserve their identities. Personal scope is appropriate only when that Amp user's Orbs should all use the same intended Fizzy actor. Avoid a workspace-wide token shared by unrelated agents.
4. Do not paste the token into a thread, command argument, shell startup file, `.fizzy.yaml`, skill, or repository. Do not run `fizzy setup` or `fizzy auth login` from setup/resume. Amp injects the saved secret; the helper never reads or persists it. No verified Fizzy exchange for Amp OIDC was found in the inspected CLI, so this procedure uses a fixed agent token.
5. Once these repository changes are made available to the selected Amp project through the parent's normal delivery process, run `.agents/setup` in a fresh native Orb. If a cached snapshot lacks the binary, run `bash scripts/setup-fizzy-orb.sh` inside that exact Orb. The installer is Linux-only. Setup-file edits alone may leave an existing cached snapshot in use; this task did not delete snapshots. For an existing Orb whose secret entries changed, run `amp orb restart-processes` from its Terminal to reload them. See [secret refresh](https://ampcode.com/docs/orbs/handling-secrets) and [snapshot lifecycle](https://ampcode.com/docs/orbs/customizing).

The exact unresolved owner inputs are the target Amp project, the intended agent token, its account slug and expected Fizzy user ID. They were not supplied to this run. The secret value must be entered directly in Amp settings; it is not needed in the handoff.

## Hosted skill delivery

The parent owns the Cara Fizzy skill and its 4.0.1 corrections. After that work is verified, prepare a hosted **personal skill import including its referenced files**, review it, and publish only under separate owner authorization. Test it in an Amp Orb before a workspace admin publishes it for everyone. Existing threads need a skill reload; new threads load published hosted skills. This is Amp's [hosted import workflow](https://ampcode.com/docs/customize/global-plugins-and-skills); a local install or symlink alone does not provide cross-machine delivery.

Do not run the CLI's embedded skill installer over Cara. The repo installs only the CLI and suppresses its implicit refresh. It neither forks the parent-owned skill nor publishes any hosted content. The parent's old references read during investigation still described `success`; **4.0.1 envelopes use `ok`**, as the isolated executable probe confirmed. The parent should use the updated 4.0.1 references for live commands.

## Bounded live smoke check — pending

Run in the selected native Orb after the skill is loaded. Keep shell tracing disabled. First verify the pin/marker and the presence of injected configuration; these commands do not print secret values:

```bash
set +x
unset FIZZY_DEBUG
bash scripts/setup-fizzy-orb.sh --check
test -n "${FIZZY_TOKEN:-}" && test -n "${FIZZY_PROFILE:-}"
```

Stop if any check fails. Inspect only the selected configuration and returned account identities:

```bash
"$HOME/.local/bin/fizzy" config show --json \
  --jq '{ok, profile: .data.profile, account: .data.account}'
"$HOME/.local/bin/fizzy" identity show --json \
  --jq '{ok, accounts: [.data.accounts[] | {slug, acting_user_id: .user.id}]}'
```

Require `ok: true`, the intended account and the owner's expected agent user ID. A token's actor is independent of its account/profile label. On mismatch, stop; do not fall back to another identity. Only after a match, perform one read-only page:

```bash
"$HOME/.local/bin/fizzy" board list --page 1 --json \
  --jq '{ok, count: (.data | length)}'
```

Record the version, account/user match, success/count and whether the hosted skill loaded. No card, board, comment, or other resource mutations are part of this check.

## Validation completed

- Downloaded the published 4.0.1 Linux amd64 and arm64 archives into a temporary directory and verified both SHA-256 digests against release metadata. Each contains a regular `fizzy` executable. The [release](https://github.com/basecamp/fizzy-cli/releases/tag/v4.0.1) is the pin's source.
- Tested the real, checksum-verified Darwin arm64 4.0.1 release **only in temporary homes**, with a synthetic token and a loopback HTTP server. Verified fresh profile/account routing, the bearer credential's presence without printing it, the `ok` envelope, preservation of a custom skill behind a symlink, and absence of a credentials directory. This proves CLI behavior locally, not Linux execution or live Fizzy access.
- `python3 scripts/fizzy_orb_test.py` exercises platform rejection, missing-binary check mode, marker repair/idempotence, legacy config path handling, symlink refusal, corrupt-download preservation, and a verified fixture archive install. Set `AMUX_FIZZY_TEST_BINARY` to a separately obtained 4.0.1 executable for the real CLI probe; without it that test skips. All seven tests passed with that probe enabled. On macOS the fixtures use `shasum -a 256` for Debian's GNU checksum flag contract; the production Linux installer uses `sha256sum`.
- `bash -n scripts/setup-fizzy-orb.sh .agents/setup .agents/resume` and `git diff --check` passed.
- `go test ./scripts` fails in existing backup-removal helper tests because this shell selects Python 3.9.6, which rejects `os.path.realpath(..., strict=...)`. The four failing top-level tests are `TestBackupRemovalRefsDryRunApplyIdempotencyAndParity`, `TestBackupRemovalRefsDeclineConflictAndDriftFailClosed`, `TestBackupRemovalRefsPruneRequiresCompleteSetAndRejectsUnsafePaths`, and `TestBackupRemovalRefsMixedSetAndMultiRefAtomicSuccess`. These failures are outside the changed Fizzy files; no runner/backup code was changed. Rerun that suite with Python 3.10+ on PATH.

No native Amp `create_thread` tool is available in this session. Live Orb creation/authentication was not attempted; no alternative executor or Amux runner was launched. The installed amux skill requires authenticated native creation and prohibits switching executors when it is unavailable. No full setup hook was run on macOS, no global binary/auth/skill was modified, and nothing was committed or published. DCG and ShellCheck were not available on this shell's PATH; neither was installed as part of this bounded task.

## Source evidence for the parent

Inspected the parent's read-only 4.0.1 `upstream-source` snapshot. Relevant upstream files are [root.go](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/commands/root.go) (`resolveProfile`, token precedence, `PersistentPostRun`), [skill.go](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/commands/skill.go) (version marker and writes through global skill paths), and [config.go](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/config/config.go) (`ConfigPath`'s legacy fallback). The machine-local parent source was read, not edited.

## Parent continuation

The child is recorded as succeeded in Tycho. The parent reran `go test ./scripts` with the existing `/opt/homebrew/bin/python3.13` exposed as `python3` through a temporary PATH directory. The full script suite passed in 35.651 seconds; no Python installation or source workaround was needed. This resolves the earlier interpreter-dependent test failure.

The parent discovered the writable Amp personal skills repository at `https://ampcode.com/git/@zainfathoni/-/skills`, cloned it locally, and prepared the complete Cara Fizzy skill on branch `fizzy-4.0.1`. All copied files match Cara by SHA-256; internal reference links resolve and skill validation passes. The draft is at `/Users/zain/.local/state/fizzy-upgrade-20260912/amp-user-skills`; its portable patch is `/Users/zain/.local/state/fizzy-upgrade-20260912/amp-fizzy-skill.patch`.

The hosted repository's `AGENTS.md` requires commits from a fresh Amp Orb with Thread Creator signing and prohibits an unsigned fallback. No commit or publication was attempted. Live Orb access still needs the target project and intended Fizzy identity; no token should be supplied through chat.
