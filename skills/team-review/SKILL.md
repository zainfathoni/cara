---
name: team-review
description: Reviews teammate PRs and writes author-facing findings. Use for evidence-backed inline feedback in a current-user PENDING review.
---

# Team Review

Review independently, prove defects, and save a concise `PENDING` draft. Then offer a second opinion in another Amp mode, or complete it if already requested. Submission is a separate action.

Suggested command: `/team-review <pr-number-or-url>`

Respect the task's authorization limits throughout. For source-only work, report findings and missing proof without running tests or saving a draft. This workflow does not authorize implementation, shared-runtime changes, or publication.

## 1. Review the change

First complete [Review Setup](SETUP.md): load the skill, verify access, and check out the exact PR head in this thread. It also defines initial-review ownership and requested second opinions. Stop if setup is incomplete.

Read the PR context, base and head revisions, full diff, changed files, call sites, tests, history, and repository guidance. Review correctness, regressions, authorization, data ownership, security, performance, maintainability, and tests before reading existing pending feedback.

Record severity, relevant diff range, failing scenario, effect, evidence, confidence, and required correction. Distinguish observed behavior from inference. Worker tests and DOM checks are not end-to-end (E2E) proof. State which paths were not exercised.

**Complete when:** each changed risk area has been reviewed or has an explicit residual-risk note, and each concern has an exact source mapping.

## 2. Prove defect findings

Prove one defect at a time without implementing a fix. For each testable defect, run the smallest focused unit test that exercises the actual application code and fails on the claimed behavior. Include passing controls that distinguish the defect from broken setup. Prefer a unit test or a small standalone harness over a full-stack environment when it can establish the claim.

Test doubles may replace database, queue, or provider transport boundaries, not the behavior under test. Record the exact revision, runnable setup, command, actual result, and evidence limits. Separate executed unit behavior from source-inferred, rendered, live-provider, and production effects. Remove temporary proof files and task-owned test resources after retaining the runnable evidence.

If unit proof is unavailable or cannot establish the claim, explain why and gather the smallest authorized alternative evidence. A complete code path can establish source behavior, not rendered or live-provider effects. State exactly what the evidence establishes and what remains unverified. If it does not establish the defect, keep the concern explicitly uncertain. Ask for any missing authorization before gathering evidence. Keep policy questions separate rather than inventing failing tests for them.

Recheck the canonical head and base before proof and before drafting. If either changed, refresh the review and rerun affected proof against the new revision. Old-head tests and CI are not current-head proof.

**Complete when:** every defect finding has executed proof or a justified alternative with stated limits; concerns without sufficient evidence remain explicitly uncertain with a missing-evidence record.

## 3. Write author-facing findings

Order findings by severity. Keep each inline comment focused on one concern and attach it to the relevant code range. State the defect, its effect, and the required correction. Explain the code, not the agent's internal process.

- Preserve material caveats and policy questions. Label unresolved choices as questions, not proven defects; ask for the decision needed. Do not invent failing tests for policy questions or add unsupported suspicions as findings.
- Include small failing test snippets when they demonstrate a defect. Run them on the reviewed revision and report the revision, command, and actual result. If a snippet cannot be run, label it **Unrun** and state why. Separate executed results from illustrative examples.
- Use `suggestion` blocks only for sufficiently established replacements. Use ordinary language-tagged code blocks for illustrative fixes.
- Put tests and suggested fixes inside `<details>` sections with a `<summary>` label. Keep the defect, effect, required correction, and material caveats visible outside them.
- Keep the overview brief. Put shared test setup once there, in a collapsed section. If there are no findings, say so and state testing gaps or residual risks.

**Complete when:** each comment is actionable, its evidence has an accurate status, and unresolved questions remain explicit.

## 4. Save the pending review

Follow [`self-review`](../self-review/SKILL.md) with the completed finding set. It is the sole authority for draft inventory, in-place changes, suggestion mechanics, and exact verification. Read the existing draft before editing and preserve others' changes through that workflow.

Report the verified review link and `PENDING` state. State any verification gap instead of claiming completion.

## 5. Offer or complete the second opinion

After the draft is saved and verified, or after reporting source-only findings when drafting is not authorized, offer a second opinion unless the user has already requested or declined it for this review. Select its Amp mode through [Review Setup](SETUP.md#4-keep-initial-review-and-second-opinions-distinct). An offer is not permission to create a consultant. If it was not requested, include the proposed mode with the recommendation and leave any draft pending.

If requested, consult on the saved draft, or on private findings for source-only work. Follow the user's named consultation prompt when supplied, within the review's authorization limits. Give the consultant that exact material, available runnable proof and results, reviewed revisions, and remaining gaps. Follow [Review Setup](SETUP.md#4-keep-initial-review-and-second-opinions-distinct) for checkout and ownership requirements. Keep the consultation read-only unless separately authorized.

Wait for the response and recheck the canonical head and base. On drift, refresh affected evidence and consultation conclusions before using them; label old-revision advice as stale. Assess each concern, then make justified corrections to private findings, or to an authorized existing draft through `self-review` with saved-state verification. Report the consultant link, conclusion, corrections, and unresolved concerns. Consultation advice does not authorize implementation, draft writes, or submission.

**Complete when:** the second opinion was offered, declined, or completed and assessed. If a requested consultation is blocked, report the blocker rather than claiming the review cadence is complete.

## 6. Recommend a decision

Recommend `COMMENT`, `APPROVE`, or `REQUEST_CHANGES`. Do not recommend approval while correctness, security, data-integrity, authorization, or data-ownership concerns remain unresolved.

Present the verdict, findings, executed evidence and limits, consultation status, and unresolved choices so the user can decide whether to submit or revise. Keep internal discussion out of author-facing text. Follow any explicitly requested presentation or submission prompt within these limits.

Leave the draft pending unless the user explicitly authorizes a named event. For submission, follow [`self-review`'s submission boundary](../self-review/SKILL.md#explicit-submission-boundary).
