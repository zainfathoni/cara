# Scoped Fizzy runtime

Use Python 3.9+ and the scripts shipped with the hosted Fizzy skill. The runner works from any Amp project; the current repository never chooses the account, actor, or board.

```bash
python3 /path/to/fizzy/scripts/install_fizzy.py --check
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work identity show
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope personal board list --all
```

`install_fizzy.py` without `--check` installs on demand. The runner also installs automatically when needed, after checking that its selected runtime secret exists. Linux x64/arm64 installs use `~/.local/share/cara/fizzy/4.0.1/linux_ARCH/fizzy`; macOS uses the existing direct Homebrew 4.0.1 executable. Nothing is added to PATH, shell startup files, or project hooks. macOS installation/upgrade is the owner's responsibility; this installer never invokes Homebrew or changes its files.

## Scope and credentials

| Scope | Board routing | Required runtime environment variable | Verified actor ID |
| --- | --- | --- | --- |
| `work` | Only Work, `03fj2n6bhaen2sq6jb9zs1eon` | `FIZZY_REDALERT_TOKEN` | `03fj2nej4tfeyw5paunpl06i3` (Red Alert) |
| `personal` | Every other board | `FIZZY_WHEELJACK_TOKEN` | `03fipgbrb5fhrokehz4plyjht` (Wheeljack) |

The account is always `6104728`, the API host is always `https://app.fizzy.do`, and identity validation accepts exactly `6104728` or `/6104728` as the API's account slug. Each invocation verifies the acting user before the requested operation. Existing card targets are looked up by **number**, and their returned number and board must match. Board targets are also read before execution. Cross-scope moves are refused.

Start every invocation with `--scope work` or `--scope personal`. There is no default or mixed scope. Split a mixed request into separate invocations. `work` supplies the pinned Work board when an operation needs `--board`; `personal` requires an explicit `--board` for card list/create, columns, board lanes/accesses, and activity.

Both secrets stay in process memory/environment. Only the selected token reaches the upstream process, as `FIZZY_TOKEN`; it never appears in command arguments or a credential file. The child receives a fresh temporary HOME and working directory, an empty local configuration, disabled keyring/update notifier, and a private `4.0.1` version marker. This prevents upstream saved-credential migration and automatic rewriting of customized skills. The temporary state is removed on ordinary exit; even interrupted leftover state contains no saved credentials. No shared version marker or installed skill is changed.

Ambient Fizzy settings, saved profiles, project `.fizzy.yaml`, proxies, debug settings, and other process secrets are not passed through. The runner accepts no token, profile, account, host, or binary override. This is a routing guard for cooperating agents, not an OS sandbox against code that bypasses the runner.

## Supported commands

Commands use canonical names and long flags. Use `--flag value` or `--flag=value`, once per flag. Boolean flags accept bare `--flag` or `--flag=true|false`. Every response is a JSON envelope; `--json` is optional. Pipe the result to an external `jq` for projections. Upstream `--jq`, `--agent`, `--quiet`, `--markdown`, debug, aliases, shorthand flags, and `--help` passthrough are intentionally unsupported. Use the runner's top-level `--help` or this inventory.

`PAGE` below means `--page N` and `--all`, except where only `--page` is listed. Pagination and status remain separate: `--all` means every page of the current query, not every status. Discovery (`board list` and `search`) filters the returned page/results to the requested scope; it retains upstream pagination context. An empty scoped page does not imply later pages are empty. Identity, account, user, and tag reads are account-level metadata and are not board-filtered.

| Command | Supported operation flags |
| --- | --- |
| `identity show`, `account show` | None |
| `user list`, `tag list`, `board list` | PAGE |
| `user show USER_ID`, `board show BOARD_ID` | None |
| `search 'QUERY'` | One quoted query; results must expose a board relationship |
| `board create` | `--name` required; `--all_access true\|false`, `--auto_postpone_period_in_days`; personal only |
| `board update BOARD_ID` | `--name`, `--all_access true\|false`, `--auto_postpone_period_in_days` |
| `board accesses` | `--board`, `--page` |
| `board closed`, `board postponed`, `board stream` | `--board`, PAGE |
| `column list`, `column show COLUMN_ID` | `--board` |
| `column create` | `--board`, `--name` required; `--color` |
| `column update COLUMN_ID` | `--board`, `--name`, `--color` |
| `activity list` | `--board`, `--creator`, PAGE |
| `card list` | `--board`, `--column`, `--tag`, `--indexed-by` (or `--status`), `--assignee`, `--search`, `--sort`, `--creator`, `--closer`, `--created`, `--closed`, `--unassigned`, PAGE |
| `card show NUMBER` | None |
| `card create` | `--board`, `--title` required; `--description` or `--description_file` |
| `card update NUMBER` | `--title`, `--description` or `--description_file` |
| `card move NUMBER` | `--to BOARD_ID` required; source and destination must share scope |
| `card column NUMBER` | `--column COLUMN_ID` required; verifies membership in the card's board; canonical pseudo columns `not-now`, `maybe`, `done` also work |
| `card assign NUMBER`, `card tag NUMBER` | `--user USER_ID` or `--tag NAME`, respectively |
| `card close/reopen/postpone/untriage/self-assign/watch/unwatch/pin/unpin/golden/ungolden/publish/mark-read/mark-unread NUMBER` | None; choose one action |
| `comment list` | `--card NUMBER` required, PAGE |
| `comment show COMMENT_ID` | `--card NUMBER` required |
| `comment create`, `comment update COMMENT_ID` | `--card NUMBER` and either `--body` or `--body_file` required |
| `step list`, `step show STEP_ID` | `--card NUMBER` required |
| `step create` | `--card NUMBER`, `--content` required; `--completed` |
| `step update STEP_ID` | `--card NUMBER` required; `--content`, `--completed`, or `--not_completed` |

Descriptions and comment bodies pass native Markdown or HTML directly to upstream 4.0.1. File paths resolve relative to the caller's directory before the child changes directories. Use `--not_completed` to clear a step; upstream `--completed=false` does not explicitly clear it. Assignment/tag actions retain upstream toggle semantics: discover the current state first.

```bash
# Replace /path/to/fizzy with the loaded hosted skill's directory.
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work card list --all
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope personal card list \
  --board 03fjt5wkvxaq0zgzrymmikn8i --indexed-by closed --all
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope personal search 'Cara'

# Mutation examples only: choose and verify the actual card number first.
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work card create \
  --title 'Review rollout' --description_file ./rollout.md
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work card update 579 \
  --description '**Next:** review the rollout.'
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work comment create \
  --card 579 --body '**Checked:** the rollout is ready.'
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work step create \
  --card 579 --content 'Confirm rollout'
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work card close 579
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work card show 579
```

After every mutation, use the scoped show/list command to verify the persisted fields, status, or child relationship. The runner checks routing and the CLI's success envelope; it does not compare requested content with a post-write read. A failed or timed-out mutation may already have reached Fizzy: read back before retrying.

## Deliberate limits and sources

Unsupported operations fail closed: deletion, attachments/uploads/downloads, reactions, notification commands, migration, webhooks, credential/config/setup/skill commands, and any flag absent from this inventory. Search/list discovery requires a usable board ID and fails closed on unknown response shapes. Card-list filter values reject URL query delimiters (`&`, `#`, `%`, `?`, CR/LF) because upstream 4.0.1 concatenates those filters into its request URL; use `search` for free text containing them. Resource IDs must be lowercase alphanumeric strings of 20–32 characters; card numbers must be positive decimal numbers.

Routing validation and a mutation are separate API requests. If another actor moves a card between them, this client cannot enforce an atomic board precondition. No live mutation was used to validate this implementation.

Installation requires Python 3.9+, normal system TLS trust, and direct HTTPS access to GitHub release assets on Linux. The installer verifies official archive SHA-256 pins, extracts only the regular `fizzy` member without unpacking arbitrary paths, verifies the derived executable hash, checks the version, and replaces the private binary atomically. Existing Linux binaries are hash-checked before execution. macOS trusts the existing Homebrew package and checks its exact version; it does not download or rehash a Homebrew release archive.

Primary sources: [official 4.0.1 release](https://github.com/basecamp/fizzy-cli/releases/tag/v4.0.1), [official digests](https://github.com/basecamp/fizzy-cli/releases/download/v4.0.1/checksums.txt), [upstream configuration](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/config/config.go), [profile/token resolution](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/commands/root.go), [skill refresh](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/commands/skill.go), and [native Markdown conversion](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/commands/markdown.go).
