# Evidence Templates

Read this reference while composing the local draft or the PR's `## E2E evidence` section. Adapt labels to the repository and omit fields that do not apply.

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

## PR body section

Place this near the repository's QA, validation, or checklist section without replacing template content:

````md
## E2E evidence

<details>
<summary>Development — <scenario> — <passed | pending | blocked></summary>

Verdict: `<passed with a scenario-scoped result | pending or blocked with a reason>`

Relevant client configuration:
- `<browser engine/version, viewport, and screen reader when needed>`

Changed-behavior coverage:

| User-visible change | Executed result and evidence reference | Status |
| --- | --- | --- |
| `<changed behavior>` | `<observed result plus attachment link, DOM assertion output, or human-listening result; use the reason when not executed>` | `<passed, pending, or blocked>` |

Reproduction context:
- Route/surface: `<route and exact surface>`
- Fixture/data: `<fixture or record>`

Console/network notes:
- `<notable warnings or none>`

Evidence:
- `<scenario-scoped screenshot, recording, assertion, or listening result and reviewer-safe reference>`

</details>

<details>
<summary>Staging — <scenario> — pending</summary>

Verdict: `Pending staging deployment: <reason>`

</details>
````

Use `Manual browser verification evidence` when that is the accurate summary. For baseline/candidate comparisons, state both URLs and explain any parity gap. Label focused after-only evidence honestly.

Use product-environment language in published evidence, not execution-infrastructure language:

- Good: `Development — Chromium 128, 1280×720 viewport: the unavailable-date error appears and focus moves to the alert.`
- Good: `Staging — DOM assertion passed for role="alert" and aria-live="assertive"; screen-reader speech remains pending human listening.`
- Bad: `Full-widget Orb Chromium verification at /home/user/...`
- Bad: `Production verification` when the scenario used a local fixture that renders a production component.

Do not publish agent or runner identities, Orb, execution-infrastructure hostnames, machine paths, infrastructure-hosted URLs, or raw operational diagnostics. Keep those in private working notes when needed. Reviewer-safe product and attachment URLs may be published; otherwise identify the product environment and route without the full URL. A reviewer-facing blocker should preserve the technical meaning without infrastructure details, for example: `Blocked: the development fixture returned HTTP 500 before the changed error state rendered.`
