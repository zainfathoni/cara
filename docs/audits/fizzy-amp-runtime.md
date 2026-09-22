# Amp-wide Fizzy runtime implementation

The skill-bundled installer and explicit-scope runner are implemented in `skills/fizzy/scripts/`. They work from any Amp project without project hooks. The parent retains ownership of secret provisioning, skill entrypoint/references, hosted publishing, and Amux cleanup. This work made no commits, pushes, remote agents, or live mutations.

## Delivered interface

```bash
python3 /path/to/fizzy/scripts/install_fizzy.py --check
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work identity show
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope personal board list --all
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope work card list --all
python3 /path/to/fizzy/scripts/fizzy_amp.py --scope personal card list \
  --board 03fjt5wkvxaq0zgzrymmikn8i --all
```

The complete bounded operation/flag inventory and native Markdown mutation examples are in [scripts/README.md](../../skills/fizzy/scripts/README.md). The runner supports identity/account/user/tag reads, scoped discovery, board and card reads/create/update, columns, comments, steps, card moves within one scope, and the documented status/toggle operations. Unsupported shapes fail closed.

## Routing and credential guarantees

| Scope | Board | Runtime secret | Acting user |
| --- | --- | --- | --- |
| `work` | Work `03fj2n6bhaen2sq6jb9zs1eon` only | `FIZZY_REDALERT_TOKEN` | Red Alert `03fj2nej4tfeyw5paunpl06i3` |
| `personal` | All other boards | `FIZZY_WHEELJACK_TOKEN` | Wheeljack `03fipgbrb5fhrokehz4plyjht` |

The initial task's Red Alert ID, `03fj2j4swdfvhq6a6rj0f4n6h`, was stale. The parent supplied the corrected live-proven ID, which this runner independently verified. Actual identity responses use `/6104728`; validation accepts exactly that form or `6104728`, rejects other path forms, requires one matching account, and checks its acting user. Duplicate matching accounts fail closed.

The runner fixes `https://app.fizzy.do` and account `6104728`. It requires one explicit scope, reads only that scope's token for the child environment, and validates identity on every invocation. Existing card targets require a successful `card show NUMBER` with the matching number and an in-scope board. Board targets are read before execution. Moves check both boards; custom destination columns must belong to the card's board. Personal board-targeted requests require a board ID; work requests may use the single pinned board implicitly.

Each upstream process uses an isolated temporary HOME and working directory. An empty local `.fizzy.yaml` stops ancestor configuration discovery. Saved profiles and credentials are unavailable; keyring and update notifier are disabled. Ambient token/profile/account/board/host/debug settings, proxies, and unrelated secrets are excluded. Tokens never appear in argv or files. Upstream stderr is not forwarded; failure messages expose a bounded error code and advise read-back before retrying a mutation. Returned token values are redacted.

The runtime writes the non-secret `.last-run-version` marker inside its newly created temporary configuration directory before invoking upstream. It never rewrites a shared marker or follows a pre-existing marker symlink. The real HOME's customized skills, saved profiles, and Homebrew binary remain untouched. Normal exit removes the temporary directory; forced termination may leave non-secret temporary state.

## Installer integrity

Linux x64 and arm64 binaries install privately under `~/.local/share/cara/fizzy/4.0.1/linux_ARCH/fizzy`. The installer verifies the official archive digest, reads only the regular `fizzy` tar member, verifies its derived binary digest, checks the exact version, and atomically installs it. Every reuse checks the binary digest again. Installer-owned symlink paths are rejected. The download has no ambient proxy/config or URL override and rejects HTTPS downgrades.

| Linux architecture | Official archive SHA-256 | Derived executable SHA-256 |
| --- | --- | --- |
| amd64 | `8a3a6b48d6eb732a189a3b18d863a1db6497a55926fd6efa4ace92e9d0a30572` | `928ac813a7aac1f0c13db5974d6f40b16e77eda21f625ec01a49b7c365f2a9a7` |
| arm64 | `b96a0522929b28931a68fc11c2c5b957990d10caa831629252831631bba89dde` | `320a3ed541ea71b15519c65cf27cac8155f0f0189a9c2fad2d317a7a0c41acc0` |

Both official Linux archives were downloaded and verified during implementation; their extracted executable hashes produced the derived pins above. No Linux executable was run on this macOS host. On macOS, the installer resolves an existing Homebrew `bin/fizzy` link into `Caskroom/fizzy` or `Cellar/fizzy`, validates 4.0.1, and returns the direct executable. It never invokes Homebrew or modifies its managed files.

Primary evidence: [official release](https://github.com/basecamp/fizzy-cli/releases/tag/v4.0.1), [official checksums](https://github.com/basecamp/fizzy-cli/releases/download/v4.0.1/checksums.txt), [configuration loading](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/config/config.go), [profile/token precedence](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/commands/root.go), [automatic skill refresh](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/commands/skill.go), and [Markdown support](https://github.com/basecamp/fizzy-cli/blob/v4.0.1/internal/commands/markdown.go). Implementation also inspected the supplied read-only upstream source and prior Amux installer/tests; no Amux files were modified.

## Validation

```bash
python3 -B -m unittest discover -s setup/tests -p test_fizzy_amp.py -v
```

All **20 tests passed**, with no skips on this host. Tests cover corrected identities and real slash-prefixed slugs; stale/wrong actors; card-number resolution before mutation; wrong-board and cross-scope rejection; scoped discovery; column membership; comments/steps/status routing; Markdown file paths; unsupported operations, flags, duplicates and query injection; absent secrets; isolated configuration and secret delivery; safe failure handling; Linux x64/arm64 installation fixtures, checksum failure, idempotency and symlink rejection; and unchanged direct Homebrew files.

The real Homebrew 4.0.1 executable also sent requests to a synthetic loopback HTTP server. Those tests verified pinned account request paths, bearer authentication, native Markdown conversion for card descriptions and comments, step update and card-close endpoints, preservation of a symlinked customized skill, and absence of token/credential files. The loopback override exists only as an in-memory test patch; the production runner exposes no endpoint override.

Safe live reads independently verified both expected actors, scoped board discovery, Work and Projects board/card/column reads, scoped searches, and card/comment/step reads in both scopes. Work returned seven open cards; Projects returned an empty open-card list. Personal search returned three Cara matches on other personal boards; one supplied the personal card read target. Credentials were loaded through the parent-authorized local environment without printing or saving them. These reads did not mutate live cards.

## Limits and parent handoff

- Python 3.9+ is required. Linux downloads need system TLS trust and direct GitHub release access. Linux platform behavior is fixture-tested; native Orb execution/publishing remains with the parent. macOS validates the existing Homebrew version rather than downloading and verifying a release archive.
- The inventory deliberately excludes deletion, attachments, uploads/downloads, reactions, notifications, migration, webhooks, config/auth/setup, and general CLI passthrough. JSON envelopes are the only output format; use external `jq`. Native Markdown **input** is supported.
- Search and board discovery filter their returned response by scope while retaining pagination context. Account/user/tag metadata is account-wide. Missing board relationships fail closed. Card-list filters containing raw query delimiters are refused because upstream concatenates their values into URLs.
- Routing checks and mutation are separate requests. A concurrent actor could move a card after its check; the upstream API/CLI offers no atomic board precondition here. The caller must perform the skill's read-after-write verification. Failed/timed-out writes must be read back before retrying.
- Publish the entire reviewed hosted skill including `scripts/`; no per-project setup/resume hooks are needed. User-level secret provisioning, final reference integration, hosted publication and Amux cleanup remain parent-owned.
