# Deterministic Browser Production Reference

Read this when selecting a browser renderer or using the accepted Cukup/Desk visual reference. Reuse the method with the owning project's design contract. This is not a bundled renderer or a universal theme.

## Authority and acceptance

- [Cukup production and review thread](https://ampcode.com/threads/T-01a0de56-e932-77d6-90f3-b3a396cabd54): Zain reported watching the narrated cut and said it looked good. This is viewing acceptance, not proof of an earlier storyboard gate or all-device playback.
- [Cukup PR31](https://github.com/zainfathoni/cukup/pull/31): the production and integration reference below uses its [final head](https://github.com/zainfathoni/cukup/commit/7b02828856256046c37a6f46a132dfc84ed50ba6), not moving `main`.
- [BTA Desk design authority](https://github.com/zainfathoni/bta-notes/blob/d7c48febae80b14024848faa178adf1797ede20a/desk/DESIGN_SYSTEM.md): read the whole contract in the owning repository when making a Desk explainer. This pinned revision records the inspected baseline. Use the task's authorized revision and record changes from it. Cukup is a visual reference; Desk's rules control when they differ.

Desk uses warm paper, dark ink outlines, hard offset shadows, local fonts, an orange action accent, and restrained pastel states. Its geometry, semantic tokens, typography, and state rules remain Desk-owned. State needs readable text and a non-color cue. Missing data must not appear as zero or current data. These rules do not authorize copying Cukup's product semantics, layout, or video-specific sizes into Desk or another project. Preserve license notices for substantial copied source.

## Source ownership

At the pinned Cukup revision, `media/motion-explainer/` owns editable production assets:

- `src/scenes.js`: story, displayed and spoken copy, timing, scene actions, transitions.
- `src/index.html`, `src/explainer.css`, `src/explainer.js`: HTML/CSS/SVG renderer. `window.explainer.ready` and `window.explainer.seek(t)` are the actual interfaces.
- `product/synthetic-day.ts`, `scripts/prepare.ts`: labelled synthetic input, product-derived calculations, and a screenshot from the actual dashboard renderer and CSS.
- `scripts/voice.ts`, `scripts/voice.py`, `scripts/mix.ts`: local narration, measured clip duration, placement, and mixing.
- `scripts/docs.ts`: storyboard, WebVTT captions, and transcript from the shared timeline.
- `scripts/render.ts`, `scripts/inspect.ts`: browser frames, contact sheet, poster, encoding, and decoded-media inspection.

The service integration owns the player and packaging, not narration synthesis. In another project, locate these responsibilities there; keep its editable assets there. Keep authentic product evidence separate from explanatory overlays. A generated screenshot with synthetic input is not evidence of a real user's activity or a reproduced failure.

## Reusable sequence

1. Read the renderer, dependencies, and write paths. Select the project's tokens and fonts. Keep capture independent of a running animation clock: each `seek(t)` call must reconstruct the scene from time, including HTML positions and SVG connectors. Verify repeated and out-of-order seeks produce the same scene state.
2. Prepare evidence and approved copy. Generate narration, measure each clip, and derive scene holds from speech and reading time. Cukup checks overlap and overrun; it adds a speech/timing fingerprint to reject stale narration after edits. Apply the same freshness rule to captions. Brand pronunciation, voice, resolution, and frame rate are project decisions.
3. Generate captions, transcript, and storyboard from that timeline. Render a labelled contact sheet at settled scene times, plus dense states, transitions, and the end card. Inspect it with `view_media` and full-size crops at expected viewing size. Fix clipping, contrast, reading time, misleading claims, privacy, and contract departures. Record the brief's review decision before final encoding. This improves the historical sequence; it does not claim Cukup had prior user preview approval.
4. After the gate passes, await browser/font/image readiness. Seek to `index / fps`, capture the stage as PNG frames, and pipe them to FFmpeg with narration. Cukup uses H.264/yuv420p, AAC, and `+faststart`; choose settings for the target player, not merely the encoder. Avoid real-time screen recording when deterministic sampling is suitable.
5. Inspect decoded MP4 frames, including scene boundaries; listen and watch at normal speed. Check captions, audio coverage, measured loudness/peak, full decode, and playback on the intended surface. Save commands, dependency versions, source revision, media identity, findings, and coverage limits. Font resolution and external tool versions mean deterministic scene state does not prove identical media bytes across machines.

For decoded evidence clips, await the requested frame and browser paint before capture. The later Desk run needed two `requestAnimationFrame` callbacks after seek to prevent intermittent image mismatches. Test repeated and out-of-order timestamps around reveals, clip frames, and scene boundaries. Use the renderer's tested readiness contract rather than treating a fixed delay as proof.

Check redaction throughout motion, including closing and slide transitions. A mask that covers a settled screenshot may expose content as it moves. Preserve clip speed and significant actions unless the brief explicitly permits an edit. Record source-frame to output-frame mapping when changing frame rate. Label redacted evidence and synthetic overlays distinctly.

Measure preview throughput before encoding the full timeline. The later browser run took about 50 minutes to render a 111-second clip. Keep checking the existing process instead of starting duplicate work. Test installed font resolution; record an approved fallback when the browser cannot load the design font. Recheck dense scenes at their actual delivery size.

The following are historical Cukup commands, run from its repository root after tool and path checks. They are not commands to run in Cara. Use the authorized project's equivalent and complete the review between `contact` and `video`:

```sh
bun media/motion-explainer/scripts/prepare.ts
bun media/motion-explainer/scripts/voice.ts
bun media/motion-explainer/scripts/docs.ts
bun media/motion-explainer/scripts/render.ts contact
# Inspect the contact sheet and record the required review decision here.
bun media/motion-explainer/scripts/render.ts video
bun media/motion-explainer/scripts/render.ts poster
bun media/motion-explainer/scripts/inspect.ts
```

For exact dependencies, command options, and storage rules, read the pinned [production README](https://github.com/zainfathoni/cukup/blob/7b02828856256046c37a6f46a132dfc84ed50ba6/media/motion-explainer/README.md), [renderer](https://github.com/zainfathoni/cukup/blob/7b02828856256046c37a6f46a132dfc84ed50ba6/media/motion-explainer/scripts/render.ts), and [evidence](https://github.com/zainfathoni/cukup/blob/7b02828856256046c37a6f46a132dfc84ed50ba6/media/motion-explainer/evidence.md). Setup, downloads, and publication still require the main skill's approval boundaries.

## Factual and playback limits

Cukup's synthetic Working Time explains a union of turn intervals. It does not measure human attention, productivity, quality, wellbeing, or personal worth. Conceptual cards are not implemented task controls. Other projects need their own factual limits, supported by their own sources.

The accepted cut was 98.9 seconds. Sampling, speech transcription, encoding success, and publication do not prove uninterrupted listening, user satisfaction, or owner-device playback. In the inspected thread, the owner reported that direct MP4 playback worked on an iPhone 15 Pro Max with iOS 27, but the embedded home-page player still failed in a fresh Safari Private Browsing session. Automated Chromium and Linux WebKit checks did not reproduce that inline failure; Linux WebKit emulation was not actual iOS Safari. The owner-observed inline failure remained unresolved. Preserve that distinction rather than asserting universal compatibility. Technical validation, viewing acceptance, and permission to publish are separate records.
