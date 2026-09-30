# Validation Record

Evidence checked on 2026-09-30. The originating Amp coordinator handled the producer and bridge. A separate delivery coordinator handled user delivery. The Cara author checked their records, not the private media itself.

## Source checks

- Metadata, exact skill name, explicit invocation, size, and local Markdown links passed checks.
- Text checks found no private account values, machine paths, task IDs, branch requirements, or fixed premium-model default.
- `git diff --check` passed. Installer `--list` recognized the skill without changing an installation.
- Shell and Python examples passed syntax checks. The loudness JSON parser handled trailing progress text in a focused test.

## Original Tycho run

- One dormant native agent was prepared. The coordinator revalidated its route and created a task-digest `report_only` receipt before execution.
- Provider initialization confirmed model and working directory. Terminal usage confirmed no model substitution. One run succeeded with exit code zero. There was no relaunch or fallback.
- The producer retained narration, source, video, transcript, scene timings, and corrected validation privately. The [macOS recipe](macos-recipe.md) records its successful method.
- A revision replaced an earlier video copy. The coordinator discarded its stale approval and checked the replacement.

## Original media and handoff

The private validation record binds the final SHA-256 identity to these checks:

- Metadata and full decode passed. Every scene contained narration. Narration intervals fit scene intervals. Audio level and silence checks passed.
- The originating coordinator's full `view_media` review passed speech, synchronized motion, readable labels, factual limits, and conditional fixes.
- The delivery coordinator independently checked a matching copy and confirmed private video and transcript delivery.

The producer submitted one typed `complete` report. The originating coordinator consumed it and acknowledged it separately after technical validation. The bridge returned `acknowledged` with custody cleanup completed.

## Kokoro replacement

- The user authorized a local voice replacement. Amp reused the diagrams and preserved the original video. There was no new Tycho run or bridge operation.
- The [Kokoro recipe](kokoro-recipe.md) records tested setup, public asset download, offline generation, timing changes, and normalization.
- Its separate private record binds the final normalized MP4's SHA-256 identity to full decode, scene-audio, timing, and audiovisual checks. A later hash check confirmed that identity.
- The measured encoded true peak exceeded the filter target without detected clipping.
- The user later authorized saving and publishing the replacement asset set in its owning private project. Separate audiovisual satisfaction was not recorded. This authorization does not apply to other projects or media.

## Limits

The runs establish macOS methods and a compatibility-bridge handoff, not a native authenticated direct-return API or cross-platform support. The synthetic explanation does not reproduce the reported failure or establish its cause. The original duration missed its target but met its accepted cap.

Cara excludes private evidence, task identities, machine paths, and private task/artifact hashes. Public model revisions remain in the recipe for reproduction.
