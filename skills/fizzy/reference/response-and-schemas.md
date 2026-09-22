# Fizzy responses and schemas

Use `--json` to retain the envelope. Built-in `--jq` filters that envelope; `--quiet` or `--agent` instead unwrap `.data`.

```json
{"ok": true, "data": {}, "summary": "Resource summary", "context": {}, "breadcrumbs": []}
```

Optional pagination is under `.context.pagination`; create locations are under `.context.location`. Errors use `{"ok": false, "error": "message", "code": "NOT_FOUND"}`. Check both the process exit status and `.ok` before reading `.data`. Metadata and optional fields may be absent.

Exit codes: 1 usage, 2 not found, 3 authentication, 4 forbidden, 5 rate limit, 6 network, 7 API/general failure, 8 ambiguous match.

Breadcrumbs contain `action`, `cmd`, and `description`. Read them with `fizzy card show NUMBER --jq '.breadcrumbs'`. Resolve placeholders and apply the user's scope before running a suggested command.

## Resource Schemas

Common resource fields. Inspect actual results before relying on optional fields.

### Card Schema

**IMPORTANT:** `card list` and `card show` can omit optional relationships. Treat absent arrays with `// []` or optional iteration; use `step list --card NUMBER` when steps are needed.

| Field | Type | Description |
|-------|------|-------------|
| `number` | integer | **Use this for CLI commands** |
| `id` | string | Internal ID (in responses only) |
| `title` | string | Card title |
| `description` | string | Plain text content (**NOT an object**) |
| `description_html` | string | HTML version with attachments |
| `status` | string | Usually "published" for active cards |
| `closed` | boolean | true = card is closed |
| `golden` | boolean | true = starred/important |
| `image_url` | string/null | Header/background image URL |
| `has_more_assignees` | boolean | More assignees than shown |
| `created_at` | timestamp | ISO 8601 |
| `last_active_at` | timestamp | ISO 8601 |
| `url` | string | Web URL |
| `comments_url` | string | Comments endpoint URL |
| `board` | object | Nested Board (see below) |
| `creator` | object | Nested User (see below) |
| `assignees` | array | Array of User objects |
| `tags` | array/null | Optional tag values; inspect the returned shape before projecting IDs or names |
| `steps` | array/null | Optional in `card show`; use `step list --card NUMBER` when absent |

### Board Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Board ID (use for CLI commands) |
| `name` | string | Board name |
| `all_access` | boolean | All users have access |
| `created_at` | timestamp | ISO 8601 |
| `url` | string | Web URL |
| `creator` | object | Nested User |

### User Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | User ID (use for CLI commands) |
| `name` | string | Display name |
| `email_address` | string | Email |
| `role` | string | "owner", "admin", or "member" |
| `active` | boolean | Account is active |
| `created_at` | timestamp | ISO 8601 |
| `url` | string | Web URL |

### Comment Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Comment ID (use for CLI commands) |
| `body` | object | **Nested object with html and plain_text** |
| `body.html` | string | HTML content |
| `body.plain_text` | string | Plain text content |
| `created_at` | timestamp | ISO 8601 |
| `updated_at` | timestamp | ISO 8601 |
| `url` | string | Web URL |
| `reactions_url` | string | Reactions endpoint URL |
| `creator` | object | Nested User |
| `card` | object | Nested {id, url} |

### Step Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Step ID (use for CLI commands) |
| `content` | string | Step text |
| `completed` | boolean | Completion status |

### Column Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Column ID or pseudo ID ("not-now", "maybe", "done") |
| `name` | string | Display name |
| `kind` | string | "not_now", "triage", "closed", or custom |
| `pseudo` | boolean | true = built-in column |

### Tag Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Tag ID |
| `title` | string | Tag name |
| `created_at` | timestamp | ISO 8601 |
| `url` | string | Web URL |

### Reaction Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Reaction ID (use for CLI commands) |
| `content` | string | Emoji |
| `url` | string | Web URL |
| `reacter` | object | Nested User |

### Identity Schema (from `identity show`)

| Field | Type | Description |
|-------|------|-------------|
| `accounts` | array | Array of Account objects |
| `accounts[].id` | string | Account ID |
| `accounts[].name` | string | Account name |
| `accounts[].slug` | string | Account slug (verify against the selected profile) |
| `accounts[].user` | object | Your User in this account |

### Key Schema Differences

| Resource | Text Field | HTML Field |
|----------|------------|------------|
| Card | `.description` (string) | `.description_html` (string) |
| Comment | `.body.plain_text` (nested) | `.body.html` (nested) |
