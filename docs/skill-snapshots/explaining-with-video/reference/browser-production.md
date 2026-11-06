# Historical Browser Production Reference

> **Unmaintained snapshot.** For study only. The [snapshot warning and source record](../REFERENCE.md) apply to this file. This is not an active skill or a bundled renderer.

This public version generalizes the source's project-specific production references.
Private design documents, thread links, project commands, and acceptance details
are omitted. The owning project's design contract remains the authority.

## Source ownership

The historical browser workflow separated these responsibilities:

- Scene source: story, displayed and spoken text, timing, scene actions, and transitions.
- HTML/CSS/SVG renderer: readiness and a `seek(t)` interface that reconstructs scene state from time.
- Evidence preparation: labelled synthetic input and authentic screenshots kept separate from annotations.
- Voice and mixing: local narration, measured clip duration, placement, and mixing.
- Documentation: storyboard, WebVTT captions, and transcript from the shared timeline.
- Rendering and inspection: browser frames, contact sheet, poster, encoding, and decoded-media checks.

The player and packaging are separate from narration generation. Editable assets
belong in the owning project. A generated screenshot with synthetic input is not
evidence of a real user's activity or a reproduced failure. Preserve license
notices for substantial copied source.

## Historical sequence

1. Read the renderer, dependencies, and write paths. Select the project's tokens and fonts. Keep capture independent of a running animation clock: each `seek(t)` call reconstructs the scene from time, including HTML positions and SVG connectors. Check repeated and out-of-order seeks.
2. Prepare evidence and approved text. Generate narration, measure each clip, and derive scene holds from speech and reading time. Check overlap and overrun. Use speech-text hashes to reject stale narration after edits. Apply the same rule to captions. Voice, resolution, and frame rate are project decisions.
3. Generate captions, transcript, and storyboard from that timeline. Render a labelled contact sheet at settled scene times, plus dense states, transitions, and the end card. Inspect it at delivery size. Fix clipping, contrast, reading time, misleading claims, and privacy problems. Record the brief's review decision before final encoding.
4. After review passes, wait for browser, font, and image readiness. Seek to `index / fps`, capture PNG frames, and pipe them to FFmpeg with narration. The historical output used H.264/yuv420p, AAC, and `+faststart`. Choose settings for the target player, not only the encoder.
5. Inspect decoded MP4 frames, including scene boundaries. Listen and watch at normal speed. Check captions, audio coverage, measured loudness and peak, full decode, and playback on the intended surface. Save commands, dependency versions, source revision, media identity, findings, and coverage limits.

For decoded evidence clips, wait for the requested frame and browser paint before
capture. A historical run needed two `requestAnimationFrame` callbacks after seek.
Test repeated and out-of-order timestamps around reveals and scene boundaries.
Use the renderer's tested readiness contract, not a fixed delay as proof.

Check redaction throughout motion, including transitions. A mask that covers a
still screenshot can expose content as it moves. Preserve clip speed and
significant actions unless the brief permits an edit. Record source-frame to
output-frame mapping when changing frame rate.

Measure preview speed before encoding the full timeline. Continue to check the
existing render process instead of starting duplicate work. Check installed fonts
and record approved substitutes. Check dense scenes at their delivery size.

## Capture without a browser automation package

A renderer does not require Puppeteer or Playwright. The historical method started
Chrome or Chromium with `--headless=new --remote-debugging-port=0
--user-data-dir=<temp>`, read the port from `DevToolsActivePort`, and drove one page
over the DevTools WebSocket:

1. `Emulation.setDeviceMetricsOverride` set the output size at scale 1; `Page.navigate` loaded the local `index.html`.
2. `Runtime.evaluate` waited for renderer readiness and `document.fonts.ready`.
3. Each frame evaluated `seek(i / fps)`, waited for two `requestAnimationFrame` callbacks, and used `Page.captureScreenshot` for a PNG.
4. PNGs went to FFmpeg with `-f image2pipe -c:v png -i -`. Normalized narration and an SRT input were added, with H.264/yuv420p, AAC, `mov_text` subtitles, and `+faststart`.

Burn captions into frames when the delivery player can hide subtitle tracks. Also
keep the soft track and VTT/SRT files. PNG bytes can differ by a few antialiased
pixels between captures. Compare decoded pixels with a small tolerance in seek
checks. Deterministic scene state does not prove identical media bytes across
machines.

## Limits

Label synthetic data and conceptual controls. State factual limits from the
project's own evidence. Sampling, transcription, encoder success, and publication
do not prove uninterrupted listening, user satisfaction, or device compatibility.
Browser emulation is not actual-device testing. Technical validation, viewing
acceptance, and permission to publish are separate records.
