# Validation Record

Evidence checked on 2026-09-30. The originating Amp coordinator handled the producer and bridge. A separate delivery coordinator handled user delivery. The Cara author checked their records, not the private media itself.

## Browser workflow revision

On 2026-10-01, the Cara editor inspected the [Cukup production and review thread](https://ampcode.com/threads/T-01a0de56-e932-77d6-90f3-b3a396cabd54), PR31 sources and review response, and BTA Desk's design authority. The [browser production reference](browser-production.md) records pinned sources, actual commands, acceptance evidence, and limits. Formal PR review bodies were not available through the repository tool; the thread and author response supplied review context.

The revised workflow requires project design discovery, renderer reuse, separate authentic evidence and annotations, a contact-sheet review before final rendering, and project-owned editable assets. These are workflow requirements, not a claim that the earlier Tycho run used the browser method or that Cukup had prior storyboard approval. No Tycho agent or video render was started for that skill edit.

## Browser run and retained package

On 2026-10-02, the editor reviewed the completed October 1 Desk run's coordinator record and fetched its authorized private source package. The package remained in the owning private repository. The editor checked its exact size and whole-file hash, all 411 ZIP entries' CRCs, and all 409 manifest-listed files' sizes and hashes. `DELIVERY.txt` was outside the member manifest but covered by the whole-ZIP checksum. The packaged MP4 matched the independently reviewed video.

The production record showed one provider initialization and result, no recorded structured correction, separate bridge and terminal schemas, hash-bound preview approval, and later report consumption and acknowledgment. It used an adapted deterministic browser renderer with local Kokoro narration, not the earlier Python slide renderer. Thirteen seek timestamps passed repeated and out-of-order comparisons after a browser paint-settle correction.

The 111.3-second output passed full decode, scene-audio, timing, caption, and full normal-speed audiovisual/privacy review. Encoded loudness was -16.01 LUFS with -2.34 dBTP. Player controls and end-to-end playback passed, but 2,689 dropped frames left smooth headless playback unproved. Small embedded text remained limited at 390px. Actual-device and iOS playback were not tested. The user later preferred the Tycho version; this is not universal device acceptance.

The recorded provider time was 94m03s; rendering took about 50 minutes. Reported list cost was $8.65, not billing proof, and excluded coordinator/review work. A delivery URL previously returned different bytes, which required exact native-file verification. These observations support the identity, preview, process-monitoring, and retention requirements. They are not new application tests or authorization to repeat the run.

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
