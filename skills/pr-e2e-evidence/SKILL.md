---
name: pr-e2e-evidence
description: Collects and publishes browser-facing PR E2E evidence to GitHub or Google Drive. Use for static pre-merge screenshots, baseline/candidate UI comparison, bounded interaction video, or post-deployment verification.
---

# PR E2E Evidence

Produce a compact, reproducible browser record that lets a reviewer judge the PR without reconstructing the test session.

## Evidence Contract

- Populate the evidence section with browser verification; add implementation verification when the user explicitly requests it.
- Inventory the final diff's user-visible behavior changes and map each one to decisive executed evidence or an explicit pending item or blocker. Include changed success, error, loading, empty, focus, and accessibility states; do not let evidence for the primary flow stand in for adjacent changed behavior.
- Name the actual product environment exercised—development, staging, or production—plus the route, browser surface, role, fixture or data, interaction mode, and result needed to reproduce each claim. Never promote a development fixture to staging or production, or call a local production-component fixture deployed verification.
- Keep execution infrastructure out of published review evidence: no agent or runner identity, Orb, execution-infrastructure hostname, or machine path in PR prose, captions, annotations, or artifact labels. Reviewer-safe product and attachment URLs are valid; for an infrastructure-hosted surface, publish the product environment and route while keeping its full URL private. Browser engine/version, viewport, and screen-reader configuration are valid when relevant to compatibility or accessibility reproduction; macOS and browser metadata do not establish a product environment.
- Keep operational diagnostics private. Summarize a technical failure accurately in published evidence without machine details, and publish only reviewer-relevant environment, scenario, result, limitation, and blocker information.
- Keep claims bounded to the scenario exercised. Record unrelated console or network noise separately and state whether it blocked the scenario.
- Provide an adjacent text verdict for every visual artifact. Prefer PR prose over baked video captions when the native interaction and result are already visible; when annotation is necessary, use labels in addition to color without covering live UI.
- Match evidence to the claim: screenshots for static appearance and contrast, recordings for focus movement or timing, DOM assertions for role, live-region, and focus semantics, and human listening for actual screen-reader speech. Fixture status text is not proof of a production announcement.
- Treat GitHub attachment URLs as shareable. Never capture secrets or sensitive merchant or customer data.

## Screenshot or Video Gate

Use screenshots by default. Prefer one cropped, annotated before/after composite when a decision point and result tell the story together; focused after-only evidence is valid when labeled honestly.

Choose video when motion, timing, focus movement, or a multi-stage interaction is itself the evidence: navigation guards, loading transitions, save/discard lifecycles, animation, or layout shifts. Keep a decisive still and text verdict as the canonical review record. Treat the named scenario as the video's full coverage boundary.

## Ordered Evidence Process

### 1. Discover the local contract

Inspect the repository's PR template and documented QA, deployment, route, role, tenant/account, feature-flag, fixture, and evidence conventions. Check for an existing PR before creating one:

```bash
gh pr list --head "$(git branch --show-current)" --json number,title,url,state
```

If no PR exists and PR creation is in scope, create one while preserving the template. Ask one narrow question when the relevant environment or browser surface remains ambiguous after discovery.

**Complete when:** the PR target, template placement, environment, exact browser surface, access context, and required deployment follow-up are known.

### 2. Define the proof

Inspect the final diff and list each user-visible behavior it changes. For every item, write a bounded scenario with its starting state, action, expected result, route, fixture/data, and meaningful console or network checks, then assign decisive evidence or mark it pending or blocked with a reason. Include changed error, loading, empty, invalidation, focus, contrast, and announcement behavior instead of documenting only the happy path. For a regression comparison, identify the stable baseline and candidate and align viewport, scroll position, filters, dates, account, role, flags, and UI mode as closely as practical.

**Complete when:** every user-visible change in the final diff maps to one reproducible scenario and decisive evidence, pending item, or blocker, and any unavoidable baseline/candidate mismatch is recorded.

### 3. Choose the smallest decisive medium

Apply the screenshot-or-video gate above. Use the closest relevant browser environment and label it by its actual product tier: development (including a local or preview fixture), staging, or production.

- For screenshots or manual before/after comparison, read [`reference/screenshots.md`](reference/screenshots.md) before capture.
- For temporal evidence, read [`reference/video.md`](reference/video.md) before recording.

**Complete when:** each scenario has the smallest decisive evidence type or combination, and every applicable screenshot or video reference has been read.

### 4. Capture and inspect

Exercise the real interaction mode and capture only the state needed to prove the result. Ground the exact surface before claiming coverage: related widgets or routes are separate claims. For accessibility evidence, distinguish computed DOM semantics from observed visual behavior and actual assistive-technology output. Inspect final media at normal review size; recapture evidence that shows stale loading, the wrong state, hidden labels, or misleading crops.

**Complete when:** every passed claim has inspected executed evidence showing the named surface, action or comparison, and result with no sensitive data, and every remaining changed behavior is explicitly pending or blocked with a reason.

### 5. Compose the local draft

Create `docs/tests/<platform>-<id>/<file>.md`, store draft screenshots in the same evidence area, and embed them with relative paths. Record branch and commit, URLs, scenario, result, reproduction context, console/network notes, limitations, and cleanup. Read [`reference/pr-templates.md`](reference/pr-templates.md) when composing the draft or PR section.

Treat this directory as working material for the final PR evidence rather than the final destination. Private operational notes may retain local paths or execution diagnostics when needed to finish the work, but remove them when transferring evidence into reviewer-facing prose, captions, annotations, or filenames.

**Complete when:** the local Markdown renders as a self-contained review draft and every media reference resolves relatively.

### 6. Publish the pre-merge evidence

Make the open PR body the default pre-merge evidence location. A repository convention or explicit user request may select an intentional comment, Google Drive archive, or Google Docs review instead. Transfer the structured evidence and embed renderable media. For Google Docs response synchronization, hand the audited package inventory and artifact mapping to the `audit-doc-sync` skill.

- For GitHub-hosted attachments, read and follow [`reference/github-publishing.md`](reference/github-publishing.md).
- For a Drive archive, read and follow [`reference/google-drive-docs-publishing.md`](reference/google-drive-docs-publishing.md).

Group evidence by scenario or surface, preserve the existing template, and explain what each artifact demonstrates.

**Complete when:** the chosen review location renders the structured evidence and mapped media, preserves every final-diff behavior's executed result and evidence reference or explicit pending/blocker reason, has an independently verified access boundary, and leaves existing content intact.

### 7. Follow the deployment

When a candidate deployment, staging, or production verification is required, keep its actual product environment marked pending until it is ready, then repeat the same bounded scenario there. Use the closest supported equivalent when a surface is unavailable and explain the difference.

Update the local draft while it remains active. Before merge, replace pending body text with the deployed result. After merge, an intentional PR comment may record production verification chronologically; use GitHub-hosted attachments, production URLs, scenario grouping, and console/network notes.

**Complete when:** each required environment is either explicitly pending with a reason or published with a reproducible result in the correct PR location.

### 8. Clean up and report

Remove temporary browser helpers and recording overlays. Remove or leave uncommitted the `docs/tests/` draft and generated media unless the user requested a commit or the repository requires durable evidence. Retain raw local video only until upload and playback are confirmed.

Report the PR URL, environments verified, scenarios and verdicts, evidence location, deployment status, limitations, and cleanup state.

**Complete when:** temporary processes and helpers are stopped, the worktree contains only intended durable files, published evidence is still accessible, and the owner has a concise verification summary.
