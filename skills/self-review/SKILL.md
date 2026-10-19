---
name: self-review
description: Creates or updates one current-user PENDING PR review in place. Use when inline review feedback must remain unpublished.
---

# Self Review

Save verified findings in the current user's single `PENDING` review. Preserve its identity and keep feedback unpublished.

Suggested command: `/self-review <pr-number-or-url>`

## Prepare findings

Use a completed independent finding set, or follow [`team-review` step 1](../team-review/SKILL.md#1-review-the-change). Apply its [author-facing content requirements](../team-review/SKILL.md#2-write-author-facing-findings), then continue here. Do not read existing pending feedback before the independent pass is complete.

## 1. Read the existing draft

Resolve the PR, authenticated user, and reviewed revision. Use [Read the PR](REFERENCE.md#read-the-pr) for commands. Fetch all reviews, comments, and required thread state; follow pagination. Find reviews owned by that user with state `PENDING`.

- No draft: prepare to create one.
- One draft: preserve its numeric ID and node ID. Read its body and complete comment set before editing.
- Unclear ownership or more than one draft: stop without changes.

Use [draft inventory commands](REFERENCE.md#find-the-current-users-draft). Continue only when ownership, draft count, IDs, body, and comments are known.

## 2. Compare findings and saved comments

Give each finding and existing comment one disposition: retain, revise, remove, or add. Retain confirmed comments. Correct overclaims; remove stale, invalid, duplicate, or superseded feedback. Preserve material caveats, policy questions, and others' edits.

Record the intended body and full comment set before changes. Re-read the draft immediately before writing. If it changed, compare again and preserve those edits. If an edit conflicts with a required correction, stop and explain the conflict instead of overwriting it.

## 3. Save in place

Read the [in-place change reference](REFERENCE.md#reconcile-in-place) before writing. If no draft exists, [create one](REFERENCE.md#create-a-new-pending-review). Otherwise, update the same review and its comments by ID.

- Omit `event`; `PENDING` is not an event value.
- Attach new inline threads and suggestion blocks to the pending review's node ID through GraphQL.
- Never use `POST /pulls/{pull_number}/comments` for drafts; it publishes immediately.
- Never delete or replace the review as a fallback. If a required in-place change is unsupported, stop. Explain the blocker and require explicit use of `review-clear`, the sole authority for draft deletion. Repeat inventory after that separate operation succeeds.

## 4. Verify the saved review

Fetch the review, body, all comments, and thread state again. Compare them with the intended set. Completion requires:

- exactly one review, owned by the authenticated user, still `PENDING`;
- the same review ID when a draft existed;
- exact body, comment bodies, IDs, count, paths, diff sides, and line ranges;
- suggestions attached to that review with valid `suggestion` fences; and
- no missing, duplicate, stale, or accidentally public feedback.

Report findings first, the review link, ID and state, saved comment locations, relevant changes to existing feedback, and residual risks. If verification is incomplete, report the gap and stop without a destructive fallback.

## Explicit Submission Boundary

Leave the review pending by default. Submit only when the user explicitly names `COMMENT`, `APPROVE`, or `REQUEST_CHANGES`. Then [submit the existing review](REFERENCE.md#submit-only-when-explicitly-instructed) and verify its resulting state and visibility.
