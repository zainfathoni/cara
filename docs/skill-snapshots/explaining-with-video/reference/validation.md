# Historical Validation Notes

> **Unmaintained snapshot.** For study only. The [snapshot warning and source record](../REFERENCE.md) apply to this file. These are summarized reports from the private source, not checks run for this public snapshot.

## Lineage

The source replaced an earlier Tycho-based workflow with one Claude Code producer
in the current thread or one native Amp child thread. It kept brief, design,
evidence, preview, final-media, and retention checks. Earlier standing route
permissions did not transfer; each task had to name its producer route.

## Reported production findings

The private source recorded browser and macOS runs. Private task details and
links are omitted. The reported lessons were:

- Kokoro CPU narration worked with one clip per sentence. Measured clips supplied scene and caption timing; spoken-text hashes let corrections reuse unchanged clips.
- Contact-sheet inspection found clipped and overlapping boxes and unexpected font substitution before final rendering.
- Repeated and out-of-order browser seeks needed paint-readiness checks. PNG bytes could differ by a few antialiased pixels, even when scene state matched.
- Decoded final frames exposed captions that continued into the next scene. Cue timing needed explicit scene limits and a new render.
- Independent review found claims stronger than their evidence. Narration, captions, and labels had to state the limits of the sources, not claim what nobody had done.
- AAC encoding could raise the final true peak above the filter target. The encoded result needed a new measurement.
- A headless playback run dropped frames. Successful encoding did not prove smooth playback or small-screen readability.
- A delivery route once returned different bytes. Delivery needed a final size and hash check.

## Coverage limits

The historical reports did not establish universal device support. Headless
Chromium checks, browser emulation, actual-device playback, normal-speed human
listening, and user acceptance were separate forms of evidence. Font substitutes
and machine-local dependencies also limited reproduction.

This snapshot supplies no original media, renderer, private evidence, acceptance
record, or current compatibility guarantee. No video was generated or tested as
part of adding this snapshot to Cara.
