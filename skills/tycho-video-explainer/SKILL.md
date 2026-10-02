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

Record the resolved skill paths and file hashes, not only skill names. A local installation and an Amp global mirror can differ. Resolve differences before production. Record runtime, browser, renderer, font, and voice-model identities without copying secrets or private machine paths into public guidance.

Inspect existing agent, receipt, and execution state. A new workspace lacks parent uncommitted files; transfer required state through native tools. Keep private evidence in restricted local storage. Exclude secrets from prompts, logs, and media.

Get separate approval for production actions, Git updates, purchases, publication, authentication transfer, installation, or shared configuration changes. A video request alone permits none of them.

For a separately authorized voice replacement after the original handoff, use the replacement branch below instead of steps 2–4.

**Complete when:** Amp's record contains authorization, exact route, available inputs, permitted effects, and existing task state.

## 2. Save the video brief

Name the decision the video must help the user make. Check whether an existing explainer still answers it. Collect missing evidence first when it would change the options or recommendation. A video may explain an investigation request, but it must not replace that investigation. A preference for Tycho does not authorize new runs for every open item.

Read the owning project's design contract, tokens, fonts, and accepted UI before selecting a visual style. Inspect earlier media source, scripts, Git history, and linked Amp threads and PR reviews. Record the design authority, revision, production method, and actual acceptance evidence. Use the project's contract when it differs from a reference. If no contract exists, record the proposed direction as unapproved and resolve it during preview review.

Select an existing renderer that fits the contract, evidence, and authorized environment. Reuse it before creating a replacement. For deterministic browser rendering and the accepted paper/ink reference, read the [browser production reference](reference/browser-production.md). Its style is an example, not a global theme. A voice recipe does not select the renderer or visual style.

Read the evidence first. Separate observed symptoms, established causes, and hypotheses. Label each unconfirmed cause in narration and visuals. Explain its confirmation test and conditional fix. Describe a fix as tested only when evidence supports that claim.

Keep authentic screenshots, logs, and source data separate from annotations and conceptual diagrams. Retain a restricted original and source identity. Label synthetic data, reconstructions, and overlays. Cite the evidence behind each factual scene. A conceptual control must not imply an implemented feature. Use a redacted derivative for delivery and preserve the original under its access rules.

Set the audience, language, duration target, accepted cap, and output format. A 90–120-second clip is an option, not a rule. Use this sequence:

1. Symptoms.
2. Established cause or unconfirmed hypotheses.
3. Conditional fixes and the next check.

End with the exact decision, options, recommendation, and effects that need approval. Separate permission to collect evidence from permission to repair or publish. Record any cost cap, time limit, and correction allowance; leave an unspecified cap explicitly unspecified. Use measured preview render speed and planned frame count to estimate the final render time.

Require audible narration and animation that explains a change, sequence, or relationship. Require large, readable labels and enough reading time after reveals. Plan captions and a transcript; if the delivery format cannot carry them, record the limit and provide a text equivalent. Save editable scene source, narration text, timings, captions, render scripts, successful commands, and check results in the owning project's authorized media directory. Cara owns the reusable workflow, not another project's assets. Keep restricted evidence, models, caches, and bridge state outside public Git.

Specify a representative contact-sheet review before the costly final render. Include every scene, dense evidence, uncertainty labels, transitions, and the end card. Record who reviews it and whether user approval is required. Rendering tools and a contact sheet are not evidence of user acceptance.

Include input identities, route, permitted effects, output paths, checks, and the installed typed-report contract in the brief. Save its exact bytes. Compute their SHA-256 hash; this is the task digest. Preserve a brief already bound to a receipt. Stop if its recorded digest differs.

**Complete when:** Amp's record contains the saved brief, design and renderer decisions, evidence identities, asset owner, preview gate, and independently computed task digest.

## 3. Prepare, bind, and start once

Select the execution branch from recorded state:

- **Unused preparation:** reuse it only when route, originating Amp thread, and task digest match. Preserve any existing receipt binding.
- **No preparation:** prepare one dormant agent only with explicit authority. Use the exact selected route without provider execution.
- **Already started:** verify its route, origin, digest, and existing pre-run receipt before step 4. Preserve that receipt. Do not start again.
- **Mismatch or uncertain history:** preserve state. Then stop. No retry, model substitution, nested agent, or executor fallback is permitted.

For compatibility-bridge operations, read the installed [bridge protocol](https://github.com/zainfathoni/amux/blob/main/skills/amux-tycho/reference/tycho-report-bridge.md) and its helper implementation. The helper is under `experimental/tycho-report-bridge/tycho_report_bridge.py` in the installed `amux-tycho` skill. Obtain schemas there rather than from an old example.

Freeze the bridge report and provider terminal-result schemas separately when the route requires both. Record the installed correction setting; do not claim one attempt from a single manual start alone. Before binding and starting, confirm that the dormant agent still exists with the expected prompt, route, zero runs, and empty queue. Missing or changed state is a blocker, not permission to create a replacement.

For a never-started preparation, revalidate the route immediately before execution. Create a matching `report_only` receipt before execution if none exists. Its originating Amp thread owns consumption and acknowledgment. Give the producer only proof fields and the submission route. Keep owner tokens and custody locations private.

Use separate, restricted bridge storage directories. The receipt grants report submission, not Amp lifecycle or rendering authority. The brief defines permitted writes and processes. The bridge transports reports; it neither starts the provider nor proves its identity.

Start only the verified, never-started preparation. Check provider initialization for actual model and working directory. Check terminal model usage when available. Use a log parser that emits only approved fields. On failed or uncertain execution, preserve state. Then stop without another start.

**Complete when:** Amp's record contains a matching pre-run receipt and verified execution identity for the sole run.

## 4. Produce and report

For installed macOS `say`, read the [macOS recipe](reference/macos-recipe.md). For authorized local Kokoro setup and generation, read the [Kokoro recipe](reference/kokoro-recipe.md). Use the renderer selected in the brief with either voice option. Use a task-local dependency environment only with setup approval. Report missing tools or permissions instead of changing shared runtimes.

The producer generates narration, measures clip durations, and renders the preview against those timings. Inspect the representative contact sheet with `view_media` before final encoding. Check the design contract, readable evidence and captions at delivery size, scene coverage, claims, privacy, and end-card reading time. Sample transition frames or short clips where a still cannot show the behavior. Record findings, corrections, and the required review decision. If Amp is the reviewer, use the existing authorized report or artifact route; do not start another producer. Preserve the brief and receipt binding. A scope change needs new authorization, not a silent digest change.

Bind preview approval to the reviewed source, timing, and evidence hashes. After the preview gate passes, render the final video. Changes to those inputs require a new preview check. Retain editable source and successful commands in the owning repository. Invalidate stale narration and captions when copy or timing changes. A new renderer becomes verified only after execution and inspection.

Monitor the existing render with progress and process evidence. A long render does not authorize a second renderer or provider start. Report render time, provider wall time, and reported list cost separately; list cost is not billing proof.

For an existing run, monitor its state without a new launch. Require one schema-valid typed `complete` or `blocked` report. A blocked report must name its blocker. Logs, exit codes, and output files cannot replace that report. For missing or invalid submissions, preserve state. Then report the failure.

**Complete when:** the bridge records one valid typed report with the required artifacts or stated blockers.

## 5. Amp verifies and delivers

Consume the valid report through its bound route. Consumption records bridge delivery, not technical validation or user acceptance.

For a `blocked` report, assess the blocker and any partial outputs. Tell the user what remains blocked. For a `complete` report, check every required artifact and perform the following checks:

- Record the final video's SHA-256 hash with its commands and check results. A revision invalidates old media approval.
- Use `ffprobe` to check streams, codecs, dimensions, frame rate, duration, and size against the brief.
- Decode the full file with FFmpeg. Check audio levels and silence in every scene. Require narration intervals to fit scene intervals.
- Inspect decoded final frames with `view_media` for symptoms, causes or hypotheses, and fixes. Require readable, unclipped labels, synchronized captions, and uncertainty labels for unconfirmed claims. The source contact sheet does not replace final-media review.
- Review all narration and animation at normal speed. Check pronunciation, content, scene coverage, reading time, and synchronization.
- Compare the approved narration text and scene timings with the media. Check factual limits and conditional fixes. Check for exposed private evidence.
- Exercise playback, pause, seek, captions, and the text equivalent on the intended delivery surface. For web delivery, check native controls, no automatic sound, keyboard access, and representative small-screen readability. Record actual browser/device coverage; emulation does not prove owner-device playback.

Metadata, frames, or encoder success alone do not prove an audible animated video. Reaching playback end with dropped frames does not prove smooth playback. Keep failed checks and superseded findings in the evidence record. Mark unavailable or failed checks explicitly. Share a candidate as such, not as a verified result.

Recheck size and hash before delivery and after downloading from the actual delivery route. A changed file needs its own media review; a working URL is not identity proof. Deliver captions and the text equivalent as specified in the brief. Report technical checks separately from user acceptance. After handling a valid report and telling the user its outcome, acknowledge it through a separate bridge operation. The bridge attempts its own custody cleanup after acknowledgment. Acknowledgment grants no publication or other cleanup authority. For missing or invalid reports, report the failure without claiming consumption or acknowledgment.

**Complete when:** Amp's record contains the report outcome, every applicable check, user-facing delivery or blocker, and separate acknowledgment.

## 6. Preserve editable work

Keep the video and its editable source in the owning project's authorized storage. For an approved package, use an explicit file allowlist: scene and render source, license notices, redacted evidence, narration, timing, captions, transcript, player, and sanitized checks. Exclude original restricted inputs, credentials, provider logs, caches, dependencies, and receipt capabilities. Inspect included scripts and check records as well as media.

Record the archive size and SHA-256. Check archive integrity and each listed member's size and hash. Compare the manifest with the actual archive inventory; report uncovered files explicitly. Verify that the packaged video matches the reviewed video. Document machine-local paths and missing dependencies instead of claiming portable reproduction.

When Git publication is authorized, preserve unrelated checkout work, publish only the task files, then fetch and check the remote package. A disconnected runner is a blocker to local retrieval; it does not authorize another executor. Keep the producer thread until the handoff is verified. Archive it only with authorization and preserve the card owner. Once the package is retained in the repository, the user need not download it.

**Complete when:** the editable work has a verified retained location, or the report names the retention blocker. Publication and thread cleanup remain separate authorized actions.

## Local voice replacement

Use this branch only with separate approval after the original handoff. Amp preserves the original media. Amp reuses its diagrams. For Kokoro, read the [replacement recipe](reference/kokoro-recipe.md). Render to a new path. Apply the media checks and delivery instructions in step 5 without a new bridge operation. Record replacement results separately from the original receipt.

Follow the owning project's storage rules. Keep models, caches, virtual environments, and bridge state outside Git.

**Complete when:** Amp's separate replacement record contains the file identity, every media check, delivery state, and user acceptance state.

For demonstrated coverage, known limits, or acceptance history, read the [validation notes](reference/validation.md).
