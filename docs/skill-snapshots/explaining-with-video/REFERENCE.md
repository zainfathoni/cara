# Explaining with Video — Historical Snapshot

> **STALE-VERSION WARNING: This is an unmaintained reference snapshot, not an active skill.**
> Agents: use the user's installed `explaining-with-video` skill for video tasks.
> If it is unavailable, report that limit. Do not load, install, or execute this
> snapshot as a replacement. Read it only when the user asks to study this snapshot.

## Snapshot record

- Snapshot date: 2026-11-06.
- Source: the owner's private Amp User Skills repository, `explaining-with-video/`.
- Source revision: `35387a8940395ec4b04acbdb1cdc2152696d25e7` (last change to the source directory, 2026-10-29).
- Authority: the private Amp User Skills repository remains the only maintained source.
- Maintenance: no installation, synchronization, automatic refresh, or runtime link to the source.
- Public edits: private project and thread links, project-specific commands, and private task details are removed or generalized. Historical validation is summarized, not independently verified here.
- Packaging: the source's skill frontmatter and `agents/openai.yaml` are omitted. This directory is documentation outside Cara's skill directories; it contains no `SKILL.md`.

The sections below preserve the historical workflow for study. Tool names,
dependencies, defaults, and permission rules can become stale. The recipes contain
code excerpts, not a bundled renderer or a complete runnable video project.

## Historical workflow

Amp coordinates the task. One Claude Code **producer** makes the video. The producer is the current thread when it already runs as the requested Claude Code route; otherwise it is one native Amp child thread. Keep the video easy to follow when the user is tired.

Finish each step's checks before you continue. If a check fails, preserve the task state and report the blocker.

## 1. Set the scope

Make a video only on an explicit user request, or when audible narration, timed motion, or a reviewable media record is the point. For a routine explanation, use text, a box diagram, or an `amp-view` first. A view is an explanation, not test proof. Name its source and limit. Do not claim that a phone app renders an `amp-view` until a native-app check exists. Record the requested producer route (current thread, or the exact Amp project, live runner, and working directory for one child), the model, the inputs, and the permitted effects. Use the requested model or current guidance; a premium model is not a default.

Read the project guidance. Find the existing task state: earlier explainers, child threads (`find_thread` with `parent:<this thread>`), and partial media. A new workspace does not contain parent uncommitted files. Move the required files with `upload_thread_file` or `download_thread_changes`. Keep secrets out of prompts, logs, and media.

A video request alone permits only task-local production. Get separate approval for Git push, publication, purchases, paid services, credential transfer, shared configuration changes, and production actions. Task-local setup, such as a scratch dependency environment or a public free model download, is permitted when the environment allows it; record it.

For a separately approved voice replacement after delivery, use the [replacement branch](#local-voice-replacement) instead of steps 2–4.

**Complete when:** the record names the request, producer route, inputs, permitted effects, and existing task state.

## 2. Save the brief

Name the decision the video must help the user make. Check whether an existing explainer still answers it. Collect missing evidence first when it would change the recommendation. A video can explain an investigation request; it does not replace the investigation.

**Design.** Read the owning project's design contract, tokens, and fonts. Inspect earlier media source and its acceptance evidence. Use the project's contract when it differs from a reference. If no contract exists, record the direction as unapproved.

**Renderer.** Reuse an existing renderer that fits the contract and environment. For deterministic browser rendering, read the [browser production reference](reference/browser-production.md). A voice recipe does not select the renderer.

**Claims.** Separate observed symptoms, established causes, and hypotheses. Label each unconfirmed cause on screen and in narration, with its confirmation test and conditional fix. Attribute a reported result to its reporter when nobody checked it independently. State absent evidence as a limit of the sources read ("the sources do not establish a cause"), not as a claim about what nobody did; apply this to narration and on-screen labels alike. Tie each factual scene to its source link.

**Evidence.** Keep authentic screenshots, logs, and source data separate from annotations. Label conceptual diagrams as explanations, and label synthetic data and redraws. A conceptual control must not look like an implemented feature. Deliver a redacted derivative; keep the original under its access rules.

**Shape.** Set the audience, language, target duration, accepted cap, and output format. Use this sequence: symptoms; established cause or labelled hypotheses; conditional fixes and the next check. End on the decision, options, recommendation, and effects that need approval. Keep permission to collect evidence separate from permission to repair or publish.

**Media requirements.** Require audible narration and animation that shows a change, sequence, or relationship. Require large labels, readable captions, and reading time after each reveal. Plan captions and a transcript with source links; if the format cannot carry them, record the limit and supply a text equivalent.

**Storage.** Save editable scene source, narration text, timing, captions, render scripts, commands, and check results in the owning project's authorized media location. This workflow owns the reusable process, not project media. Keep models, caches, and dependency environments out of Git.

**Preview gate.** Specify a contact-sheet review before the final render: every scene, dense evidence, uncertainty labels, transitions, and the end card. Record the reviewer and whether user approval is required. A contact sheet is not user acceptance.

Save the brief's exact bytes in the task's media location and record its SHA-256. Preview and final checks refer to that identity; a scope change needs new authorization and a new brief.

**Complete when:** the record contains the saved brief and hash, design and renderer decisions, evidence sources, media location, and preview gate.

## 3. Start one producer

Select the branch from recorded state:

- **Current thread is the producer:** continue to step 4 here. Make no nested producer.
- **No producer yet:** create exactly one child with `create_thread`: `agent_mode` `external-agent:claude-code`, the requested model and effort as `features`, and the exact project, or the exact live runner and working directory from `list_runners`. The prompt gives the brief path and hash, inputs, permitted effects, the media location, and this reply route: "When finished, use `send_thread_message` to send outcome `complete` or `blocked`, artifact paths, check results, and blockers to <coordinator thread>. Do the work yourself; create no other thread."
- **Child already exists:** check its route and brief hash with `get_thread_status` or `read_thread`. Send scoped follow-ups with `send_thread_message`. Create no replacement.
- **Creation unavailable, rejected, or uncertain:** preserve state and stop. Report it. Retry, model substitution, nested producers, and executor fallback each need a new user decision.

**Complete when:** exactly one producer has the brief, and the record contains its thread link and route.

## 4. Produce

**Voice.** Use local Kokoro by default, with the [Kokoro recipe](reference/kokoro-recipe.md): `af_heart`, speed 1.1, CPU, offline generation, in a task-local environment outside Git. Use another voice only when the brief names it, for example macOS `say` on a Mac runner with the [macOS recipe](reference/macos-recipe.md). A paid voice service needs approval under step 1. Use the renderer from the brief with any voice.

1. Generate one narration clip per sentence. Measure each clip. Derive scene and caption timing from the measured clips. Bind each clip to a hash of its spoken text; after a copy edit, regenerate only the clips whose hash changed, then regenerate timing and captions.
2. Render the representative contact sheet. Inspect it at delivery size. Check the design contract, readable text and captions, scene coverage, claims, privacy, and end-card reading time. Sample transition frames where a still cannot show the motion. Record findings and fixes.
3. Pass the preview gate from the brief. Bind it to the reviewed source, timing, and narration. Changes to those inputs need a new preview check.
4. Render the final video. Watch the running render through its progress output. A long render does not authorize a second render or producer.
5. A child producer reports through its reply route. The coordinator treats that report as a claim to verify, not as proof.

Report render time separately from any reported cost; list cost is not billing proof.

**Complete when:** the final media, captions, transcript, editable source, and producer check results exist, or the producer reports a named blocker.

## 5. Verify and deliver

The coordinator checks the final media itself. A child's outputs reach the coordinator only through `download_thread_file` or `download_thread_changes`; a file in another orb does not transfer by itself.

- Record the final video's size and SHA-256. A revision makes earlier checks stale.
- Run `ffprobe`: streams, codecs, dimensions, frame rate, duration, and size against the brief.
- Decode the full file with FFmpeg. Measure loudness and true peak. Check that narration fills every scene and that narration intervals fit scene intervals.
- Inspect decoded final frames from each scene. Require readable, unclipped labels, synchronized captions, and uncertainty labels on unconfirmed claims. The source contact sheet does not replace this check.
- Compare narration text, captions, and scene timings with the brief. Check factual limits, attributions, conditional fixes, and private data.
- Exercise playback, pause, and seek on the delivery surface; for web delivery, also native controls, no autoplay sound, keyboard access, and small-screen readability. Record actual browser or device coverage; emulation is not owner-device proof.
- Check that captions and the text equivalent are delivered.

Metadata, sampled frames, or encoder success alone do not prove an audible animated video. Mark unavailable or failed checks. Share a candidate as a candidate. Recheck size and hash after the file reaches the delivery route. Report technical validation separately from user acceptance.

**Complete when:** the record contains every check result against the final hash, and the user has the delivery or the named blocker.

## 6. Preserve editable work

Keep the video and editable source in the owning project's authorized storage. For a package, use an explicit file allowlist: scene and render source, license notices, redacted evidence, narration, timing, captions, transcript, and sanitized checks. Exclude restricted originals, credentials, logs with secrets, caches, models, and dependency environments.

Record a manifest with each file's size and SHA-256. Check it against the actual inventory. Document machine-local paths and missing dependencies instead of claiming portable reproduction.

Git commits, pushes, and thread archiving need their own authorization. Keep a child producer's thread until the coordinator has verified the handoff.

**Complete when:** the editable work has a verified retained location, or the report names the retention blocker.

## Local voice replacement

Use only with separate approval after delivery. Preserve the original media and reuse its diagrams. For Kokoro, read the [replacement steps](reference/kokoro-recipe.md#4-render-the-scenes). Render to a new path. Apply step 5. Record replacement results separately from the original.

**Complete when:** the replacement record contains the file identity, every step-5 check, delivery state, and user acceptance state.

For lineage, reported coverage, and known limits, read the [historical validation notes](reference/validation.md).
