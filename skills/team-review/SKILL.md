---
name: team-review
description: Reviews teammate PRs and writes author-facing findings. Use for evidence-backed inline feedback in a current-user PENDING review.
---

# Team Review

Review the change independently. Write for the PR author, then save a `PENDING` GitHub review with inline findings and a brief overview.

Suggested command: `/team-review <pr-number-or-url>`

## 1. Review the change

Read the PR context, base and head revisions, full diff, changed files, call sites, tests, history, and repository guidance. Review correctness, regressions, authorization, data ownership, security, performance, maintainability, and tests before reading existing pending feedback.

Verify each concern against the reviewed revision. Prefer a focused failing test where it can demonstrate the defect. Use the `tdd` skill for one-test-at-a-time proof when feasible. Otherwise, use browser behavior, logs, API results, or direct code-path evidence. Remove temporary proof-only changes.

Record severity, relevant diff range, failing scenario, effect, evidence, confidence, and required correction. Distinguish observed behavior from inference. Worker tests and DOM checks are not end-to-end (E2E) proof. State which paths were not exercised.

**Complete when:** each changed risk area has been reviewed or has an explicit residual-risk note, and each finding has supporting evidence.

## 2. Write author-facing findings

Order findings by severity. Keep each inline comment focused on one concern and attach it to the relevant code range. State the defect, its effect, and the required correction. Explain the code, not the agent's internal process.

- Preserve material caveats and policy questions. Label unresolved choices as questions, not proven defects; ask for the decision needed. Do not invent failing tests for policy questions or add unsupported suspicions as findings.
- Include small failing test snippets when they demonstrate a defect. Run them on the reviewed revision and report the revision, command, and actual result. If a snippet cannot be run, label it **Unrun** and state why. Separate executed results from illustrative examples.
- Use `suggestion` blocks only for sufficiently established replacements. Use ordinary language-tagged code blocks for illustrative fixes.
- Put tests and suggested fixes inside `<details>` sections with a `<summary>` label. Keep the defect, effect, required correction, and material caveats visible outside them.
- Keep the overview brief. Put shared test setup once there, in a collapsed section. If there are no findings, say so and state testing gaps or residual risks.

**Complete when:** each comment is actionable, its evidence has an accurate status, and unresolved questions remain explicit.

## 3. Save the pending review

Follow [`self-review`](../self-review/SKILL.md) with the completed finding set. It is the sole authority for draft inventory, in-place changes, suggestion mechanics, and exact verification. Read the existing draft before editing and preserve others' changes through that workflow.

Report the verified review link and `PENDING` state. State any verification gap instead of claiming completion.

## 4. Recommend a decision

Recommend `COMMENT`, `APPROVE`, or `REQUEST_CHANGES`. Do not recommend approval while correctness, security, data-integrity, authorization, or data-ownership concerns remain unresolved.

Leave the draft pending unless the user explicitly authorizes a named event. For submission, follow [`self-review`'s submission boundary](../self-review/SKILL.md#explicit-submission-boundary).
