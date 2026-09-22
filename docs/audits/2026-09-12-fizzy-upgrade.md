# Fizzy 4.0.1 upgrade and verification

Completed local upgrade from Homebrew Fizzy CLI 2.6.1 to official Basecamp cask 4.0.1. The local `fizzy` command now uses a version-checked Cara adapter, direnv-selected credentials, and the upstream binary directly. `fizzy-md` 0.1.5 and the unlinked 2.6.1 keg remain installed for rollback; neither is in the standard command chain.

## Changes

- Installed `basecamp/tap/fizzy` after unlinking the old formula. Homebrew required Basecamp tap trust; no unrelated packages were upgraded.
- Replaced `~/.local/bin/fizzy` from Cara `setup/fizzy-wrapper.sh`. Legacy `FIZZY_ACCOUNT` maps to `FIZZY_PROFILE` after direnv loads, without changing token values. Explicitly empty tokens fail with exit 3 instead of using a personal saved credential. The adapter retains the machine's Nix direnv fallback and refuses unreviewed CLI versions.
- Updated Cara's locally owned Fizzy skill and references for v4 envelopes, profile selection, search routing, pseudo-columns, optional relationships, and command discovery. Formatting, clickable relationships, complete pagination/status scope, and mutation read-back remain required.
- Found and corrected upstream auto-refresh overwriting the symlinked Cara skill. The v4.0.1 version sentinel is present; the skill is restored and its compatibility marker is recorded. Future upgrades must update the sentinel before successful commands run. See the linked runtime procedure.
- Replaced OpenClaw's stale 1,000-line duplicate skill with shared-skill routing and retained fleet-specific steps, assignment, cross-reference, and parking rules. Updated root workspace instructions to use native Markdown support.
- Migrated OpenClaw self-check and heartbeat scripts off the old formula path. Self-check uses explicit selected-agent credentials and JSON parsing. Updated board digest envelope handling while retaining its existing outward `success` field; made assignee iteration null-safe. Updated dispatcher test fixture envelopes.

## Verification

| Check | Result |
| --- | --- |
| CLI version | 4.0.1 |
| `doctor` | Zero failures; only optional Claude plugin and default-board warnings |
| Existing personal identity | Same Zain user and account before and after |
| Existing boards | Eight accessible boards before and after |
| Write smoke test | 12 checks passed on Autobots board |
| Fixture cleanup | Card 436 deleted; subsequent show returned not-found with exit 2 |
| Write behavior | Native Markdown headings/bold, HTML heading/link preservation, comment create/read, step create/update/read, close/reopen, filtered search |
| Existing data | Six read checks passed on Work board, including existing card show and complete open/closed/postponed listings |
| Full-text search | Successful JSON response |
| Agent identity | Wheeljack and Optimus credentials resolve to their own users |
| Missing agent token | Explicit empty token exits 3 before API access; no personal-login fallback |
| Dispatcher integration | Passed with v4 response fixtures |
| Heartbeat read | Wheeljack check succeeds; API/envelope errors now propagate instead of appearing as an empty backlog |
| Board digest | Passed; Work board returned seven open cards |
| Skill refresh | Successful CLI call leaves customized Cara skill byte-for-byte unchanged |
| Static checks | Both skills validate; changed shell scripts pass syntax checks; scoped diffs pass whitespace checks |

The agent identity check initially exposed an existing bootstrap issue: Wheeljack's direnv references an environment variable that is absent unless the fleet credential source is loaded. With that source loaded, identity is correct. The adapter now fails closed when it is absent; credentials were not copied or rewritten.

No existing production cards were mutated. The disposable smoke-test card and its children were removed. Tests do not establish board migration, webhook, or exhaustive multi-account compatibility. No source changes were committed or published in this run.

## Standard procedure and artifacts

- [Runtime setup and future upgrades](../../skills/fizzy/reference/runtime-setup.md)
- [Shared skill](../../skills/fizzy/SKILL.md)
- [Local adapter](../../setup/fizzy-wrapper.sh)
- [Repeatable smoke test](../../setup/tests/fizzy-smoke.py)
- Local backups: `~/.local/state/fizzy-upgrade-20260912/`, including the old adapter and OpenClaw skill. The isolated upstream source checkout is also there.

## Amp-wide follow-up

The initial Amux project-local prototype was the wrong deployment scope and has been removed from Amux; its worktree is clean. Historical evidence is retained in [the superseded prototype report](fizzy-orbs-project-prototype.md). The full amux script suite passed with the installed Python 3.13, resolving its earlier interpreter-only failures.

The corrected implementation belongs to Cara and is being delivered through Amp personal hosted skills and user-level secrets. Red Alert handles Work; Wheeljack handles other boards. See [the Amp-wide rollout report](2026-09-12-amp-wide-fizzy.md) for secret provisioning, the published skill, live Orb evidence, and any remaining board-access limits.

Primary upstream references: [4.0.0 breaking changes](https://github.com/basecamp/fizzy-cli/releases/tag/v4.0.0), [4.0.1 release](https://github.com/basecamp/fizzy-cli/releases/tag/v4.0.1), [automatic skill refresh source](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/commands/skill.go), [Amp global skills](https://ampcode.com/news/global-plugins-and-skills), [Orb secrets](https://ampcode.com/docs/orbs/handling-secrets).
