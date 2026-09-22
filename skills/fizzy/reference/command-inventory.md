# Fizzy command discovery

In Amp, use the bounded commands and flags in [the scope runner reference](../scripts/README.md). It intentionally exposes a subset of the upstream CLI and always returns a JSON envelope. Report unsupported operations instead of bypassing identity routing.

Outside that Amp adapter, the installed 4.0.1 CLI is the command and flag authority. Discover the specific command before constructing an operation:

```bash
fizzy commands --json
fizzy card create --help
fizzy card create --help --agent
```

Use `fizzy RESOURCE ACTION --help` for the operation at hand; the catalog covers boards, cards, comments, steps, reactions, users, notifications, pins, uploads, accounts, webhooks, activity, authentication, and migration. Read [responses](response-and-schemas.md) when parsing results and [querying](querying-and-accounts.md) for status/account scope.

## Changes from 2.x

- Global account selection uses `--profile NAME`; account slugs and profile aliases are distinct. `auth login` still has an account-binding flag.
- `--json` replaces `--pretty`; the success field is `ok`.
- `search QUERY` uses ranked full-text search. Board, status, assignee, tag, sort, and pagination filters belong on `card list --search QUERY`.
- `card create --tag-ids` was removed. Inspect current tags and use the documented tag action afterward.
- The postpone pseudo-column is `not-now`; the status index remains `not_now`.
- `step list --card NUMBER` exists.
- Descriptions and comment bodies accept Markdown or HTML. Cara's card-description HTML convention remains in [formatting](card-description-formatting.md).
- `--attach PATH` appends an inline attachment; repeat for multiple files. Use manual upload/markup for exact placement.
- Board entropy flags use `--auto_postpone_period_in_days`.

## Board migration

Read [migration behavior](board-migration.md), then `fizzy migrate board --help`. Migration retains `--from` and `--to` account slugs; these are not global profile selectors. Review `--dry-run` before copying content.
