# Amp-wide Fizzy access

The owner uses one **personal hosted Amp skill** and two **user-level Amp secrets**, available across all of their Amp projects. Scope is chosen by the target Fizzy board, not by the current Git repository or Amp project.

| Scope | Boards | Acting user | Runtime secret |
| --- | --- | --- | --- |
| `work` | Work, ID `03fj2n6bhaen2sq6jb9zs1eon` | Red Alert, ID `03fj2nej4tfeyw5paunpl06i3` | `FIZZY_REDALERT_TOKEN` |
| `personal` | Every other board | Wheeljack, ID `03fipgbrb5fhrokehz4plyjht` | `FIZZY_WHEELJACK_TOKEN` |

Both identities use account slug `6104728` at `https://app.fizzy.do`. A profile label does not choose an identity: the token does. These user IDs were verified through the live identity endpoint; older fleet notes contain a stale Red Alert ID.

## Operating rule

Choose the board and scope before issuing a command. For work spanning both scopes, split the request and run each portion with its own identity. For ambiguous existing card numbers, use available task context to choose the scope; ask which board the user intends if needed. Never guess a mutation's identity from the current Amp project.

Use the skill-bundled runner rather than a raw `fizzy`, `fizzy-md`, or project wrapper. [Supported commands and flags](../scripts/README.md) define this bounded interface. It always returns the JSON envelope; filter stdout with an external `jq` pipe when needed instead of passing output-mode flags. It loads the selected secret into the child process environment, validates the actor, pins the account/API host, and checks card/board scope before mutation. It fails on a missing credential or unsupported operation; do not bypass it with a raw CLI mutation. Preserve the shared skill's read-after-write verification and formatting rules.

The runner installs its pinned Linux binary on demand after verifying the release digest. Installation comes from the hosted skill's files, so projects need no `.agents/setup` or `.agents/resume` modifications. It writes no login credentials or token files. On macOS it uses the existing validated Homebrew binary.

## Commands

Resolve the actual directory of this loaded skill; hosted skill paths can differ between Orbs. From that directory:

```bash
python3 scripts/fizzy_amp.py --scope work board list --all
python3 scripts/fizzy_amp.py --scope work card list --all
python3 scripts/fizzy_amp.py --scope personal board list --all
python3 scripts/fizzy_amp.py --scope personal card list --board BOARD_ID --all
python3 scripts/fizzy_amp.py --scope work card show CARD_NUMBER
```

Personal card listings require one explicit non-Work board. To inspect all personal boards, list them and query each returned board separately. Use `--indexed-by closed` or `not_now` and `--all` for complete status coverage. Every mutation is followed by a scoped read-back.

## Secret delivery

`FIZZY_REDALERT_TOKEN` and `FIZZY_WHEELJACK_TOKEN` are stored as **secrets**, not plain environment variables, in Amp personal settings. User-level entries override project/workspace entries of the same name. Both names are unique to these actors; there is no shared default `FIZZY_TOKEN` for Amp-wide operation.

New Orbs receive the saved values. To reload secrets in an existing Orb, use `amp orb restart-processes` in that Orb when its current task can be restarted. Local Amp sessions still need credentials supplied by the machine's existing secret environment; Amp's user-level secrets are delivered to Orbs, not automatically to the local shell.

Never print secret values, pass tokens in command arguments, or persist them in repositories, skill files, or snapshots. Verify the selected user and board before live operations.

## Hosting and updates

Cara is the source of truth; publish this entire `fizzy/` directory, including `reference/` and `scripts/`, into the owner's Amp personal skills repository. A hosted push makes the skill available in new Amp threads across projects; reload skills in an existing thread after publication. A machine-local symlink or `amp skill add --global` alone does not publish a hosted skill.

Update the CLI pin, installer digests, identity routing tests, and skill references together. Fizzy 4.0.1 auto-refreshes global skill files through symlinks; the bundled runtime uses isolated process state with the reviewed version marker to preserve this customized skill. Recheck that upstream behavior on version changes.

Sources: [Amp global skills](https://ampcode.com/docs/customize/global-plugins-and-skills), [Amp user-level secrets](https://ampcode.com/docs/orbs/handling-secrets).
