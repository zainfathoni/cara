---
name: tycho-video-explainer
description: Creates a narrated animation through Tycho for users who prefer video explanations to text.
disable-model-invocation: true
---

# Tycho Video Explainer

Amp coordinates the task. One explicitly requested Tycho agent produces the video. Keep it easy to follow when the user is tired.

Finish each step's checks before proceeding. If a check fails, preserve the task state. Then report the blocker.

## 1. Set the scope

Run Tycho only on an explicit user request. Record the authorized runner, project, working directory, harness, model, inputs, and permitted effects. Use the requested model or current guidance, not an assumed premium default.

Read the project guidance and installed `tycho` and `amux-tycho` instructions. For route safety, check the [routing policy](https://github.com/zainfathoni/amux/blob/main/skills/amux-tycho/SKILL.md) and [readiness policy](https://github.com/zainfathoni/amux/blob/main/docs/provider-executor-readiness.md). Use installed-version syntax. Resolve a broken wrapper link through that installation. Stop on an unresolved policy or version conflict.

Inspect existing agent, receipt, and execution state. A new workspace lacks parent uncommitted files; transfer required state through native tools. Keep private evidence in restricted local storage. Exclude secrets from prompts, logs, and media.

Get separate approval for production actions, Git updates, purchases, publication, authentication transfer, installation, or shared configuration changes. A video request alone permits none of them.

For a separately authorized voice replacement after the original handoff, use the replacement branch below instead of steps 2–4.

**Complete when:** Amp's record contains authorization, exact route, available inputs, permitted effects, and existing task state.

## 2. Save the video brief

Read the evidence first. Separate observed symptoms, established causes, and hypotheses. Label each unconfirmed cause in narration and visuals. Explain its confirmation test and conditional fix. Describe a fix as tested only when evidence supports that claim.

Set the audience, language, duration target, accepted cap, and output format. A 90–120-second clip is an option, not a rule. Use this sequence:

1. Symptoms.
2. Established cause or unconfirmed hypotheses.
3. Conditional fixes and the next check.

Require audible narration and animation that explains a change, sequence, or relationship. Require large, readable labels. Retain approved narration text, scene timings, render source, successful commands, and check results. A separate transcript or caption file for user delivery is optional.

Include input identities, route, permitted effects, output paths, checks, and the installed typed-report contract in the brief. Save its exact bytes. Compute their SHA-256 hash; this is the task digest. Preserve a brief already bound to a receipt. Stop if its recorded digest differs.

**Complete when:** Amp's record contains the saved brief with all fields and its independently computed task digest.

## 3. Prepare, bind, and start once

Select the execution branch from recorded state:

- **Unused preparation:** reuse it only when route, originating Amp thread, and task digest match. Preserve any existing receipt binding.
- **No preparation:** prepare one dormant agent only with explicit authority. Use the exact selected route without provider execution.
- **Already started:** verify its route, origin, digest, and existing pre-run receipt before step 4. Preserve that receipt. Do not start again.
- **Mismatch or uncertain history:** preserve state. Then stop. No retry, model substitution, nested agent, or executor fallback is permitted.

For compatibility-bridge operations, read the installed [bridge protocol](https://github.com/zainfathoni/amux/blob/main/skills/amux-tycho/reference/tycho-report-bridge.md) and its helper implementation. The helper is under `experimental/tycho-report-bridge/tycho_report_bridge.py` in the installed `amux-tycho` skill. Obtain schemas there rather than from an old example.

For a never-started preparation, revalidate the route immediately before execution. Create a matching `report_only` receipt before execution if none exists. Its originating Amp thread owns consumption and acknowledgment. Give the producer only proof fields and the submission route. Keep owner tokens and custody locations private.

Use separate, restricted bridge storage directories. The receipt grants report submission, not Amp lifecycle or rendering authority. The brief defines permitted writes and processes. The bridge transports reports; it neither starts the provider nor proves its identity.

Start only the verified, never-started preparation. Check provider initialization for actual model and working directory. Check terminal model usage when available. Use a log parser that emits only approved fields. On failed or uncertain execution, preserve state. Then stop without another start.

**Complete when:** Amp's record contains a matching pre-run receipt and verified execution identity for the sole run.

## 4. Produce and report

For installed macOS `say`, read the [macOS recipe](reference/macos-recipe.md). For authorized local Kokoro setup and generation, read the [Kokoro recipe](reference/kokoro-recipe.md). Both require a scene-specific renderer. Use a task-local dependency environment only with setup approval. Report missing tools or permissions instead of changing shared runtimes.

The producer generates narration. It measures clip durations. It renders diagrams against those timings. It retains source and successful commands. A new renderer becomes verified only after execution and inspection.

For an existing run, monitor its state without a new launch. Require one schema-valid typed `complete` or `blocked` report. A blocked report must name its blocker. Logs, exit codes, and output files cannot replace that report. For missing or invalid submissions, preserve state. Then report the failure.

**Complete when:** the bridge records one valid typed report with the required artifacts or stated blockers.

## 5. Amp verifies and delivers

Consume the valid report through its bound route. Consumption records bridge delivery, not technical validation or user acceptance.

For a `blocked` report, assess the blocker and any partial outputs. Tell the user what remains blocked. For a `complete` report, check every required artifact and perform the following checks:

- Record the final video's SHA-256 hash with its commands and check results. A revision invalidates old media approval.
- Use `ffprobe` to check streams, codecs, dimensions, frame rate, duration, and size against the brief.
- Decode the full file with FFmpeg. Check audio levels and silence in every scene. Require narration intervals to fit scene intervals.
- Inspect final frames with `view_media` for symptoms, causes or hypotheses, and fixes. Require readable, unclipped labels and uncertainty labels for unconfirmed claims.
- Review all narration and animation at normal speed. Check pronunciation, content, scene coverage, reading time, and synchronization.
- Compare the approved narration text and scene timings with the media. Check factual limits and conditional fixes. Check for exposed private evidence.

Metadata, frames, or encoder success alone do not prove an audible animated video. Mark unavailable or failed checks explicitly. Share a candidate as such, not as a verified result.

Recheck the hash before delivering a native attachment or authorized private review link. Deliver optional transcript or captions if requested. Report technical checks separately from user acceptance. After handling a valid report and telling the user its outcome, acknowledge it through a separate bridge operation. The bridge attempts its own custody cleanup after acknowledgment. Acknowledgment grants no publication or other cleanup authority. For missing or invalid reports, report the failure without claiming consumption or acknowledgment.

**Complete when:** Amp's record contains the report outcome, every applicable check, user-facing delivery or blocker, and separate acknowledgment.

## Local voice replacement

Use this branch only with separate approval after the original handoff. Amp preserves the original media. Amp reuses its diagrams. For Kokoro, read the [replacement recipe](reference/kokoro-recipe.md). Render to a new path. Apply the media checks and delivery instructions in step 5 without a new bridge operation. Record replacement results separately from the original receipt.

Follow the owning project's storage rules. Keep models, caches, virtual environments, and bridge state outside Git.

**Complete when:** Amp's separate replacement record contains the file identity, every media check, delivery state, and user acceptance state.

For demonstrated coverage, known limits, or acceptance history, read the [validation notes](reference/validation.md).
