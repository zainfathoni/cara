# Evidence Draft and PR Placement

Read this reference while composing the local draft or the PR evidence. The target repository's `.github/pull_request_template.md` is the only PR-body template. Adapt the local draft to the task; it is not a PR-body template.

## Local draft

Use a stable path such as `docs/tests/github-123/e2e-evidence.md`, `docs/tests/linear-ABC-123/e2e-evidence.md`, or `docs/tests/jira-PROJ-123/e2e-evidence.md`.

````md
# E2E evidence: <PR title or feature>

Environment:
- Product environment: `<development | staging | production>`
- Branch: `<branch>`
- Commit: `<commit>`
- Primary URL: `<url>`
- Candidate URL: `<url-if-used>`
- Baseline URL: `<url-if-used>`
- Relevant client configuration: `<browser engine/version, viewport, screen reader if needed>`

## Summary

- `<browser scenario>`: `<result>`

## Changed-behavior coverage

| User-visible change | Evidence | Status |
| --- | --- | --- |
| `<behavior, including changed error/loading/empty/a11y states>` | `<executed result and screenshot/recording/assertion/listening reference, or pending/blocker reason>` | `<passed, pending, or blocked>` |

## Evidence

### <scenario and environment>

Result:
- `<verified behavior>`

Reproduction context:
- Route/surface: `<route and exact surface>`
- Fixture/data: `<fixture, selected date/filter, or record>`

Console/network notes:
- `<notable warnings or none>`

![Scenario label](./<assets-dir>/<scenario-screenshot>.png)
````

## PR evidence placement

Read the target repository's PR template before editing the body. Preserve its headings, checklist, and existing text. Add evidence near its QA or checklist section, not as an alternative body template. For BookThatApp, use one `## E2E evidence` heading with one `<details>` block. Put a short `<summary>E2E evidence</summary>` on the next line; do not use the `open` attribute. End the block with `</details>`. Check the rendered PR to confirm that the block is closed by default, the content expands, and the media renders.

Inside that block, use one short line per changed scenario: the actual product environment, the specific result or pending reason, and a reviewer-safe link to decisive evidence. Add a route, data fixture, client configuration, or limitation only when the reviewer needs it to understand or reproduce the result. Do not paste the local coverage table, command lines, script names, or routine console and network notes into the PR. Keep those details in the local draft. State a relevant failure or blocker in plain terms; do not hide it. Write the summary, verdicts, and captions in ASD-STE100: common words, active voice, and short sentences. Keep exact product labels and technical identifiers when necessary.

For baseline/candidate comparisons, identify both product environments and explain any material mismatch. Label focused after-only evidence honestly. Do not report a pending staging result as passed.

Use product-environment language in published evidence, not execution-infrastructure language:

- Good: `Development — Chromium 128, 1280×720 viewport: the unavailable-date error appears and focus moves to the alert.`
- Good: `Staging — DOM assertion passed for role="alert" and aria-live="assertive"; screen-reader speech remains pending human listening.`
- Bad: `Full-widget Orb Chromium verification at /home/user/...`
- Bad: `Production verification` when the scenario used a local fixture that renders a production component.

Do not publish agent or runner identities, Orb, execution-infrastructure hostnames, machine paths, infrastructure-hosted URLs, or raw operational diagnostics. Keep those in private working notes when needed. Reviewer-safe product and attachment URLs may be published; otherwise identify the product environment and route without the full URL. A reviewer-facing blocker should preserve the technical meaning without infrastructure details, for example: `Blocked: the development fixture returned HTTP 500 before the changed error state rendered.`
