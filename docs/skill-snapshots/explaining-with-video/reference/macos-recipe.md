# Historical Local macOS Recipe

> **Unmaintained snapshot.** For study only. The [snapshot warning and source record](../REFERENCE.md) apply to this file. Commands describe an earlier run, not a current installation recommendation.

## 1. Prepare the renderer

The main workflow selected the renderer from the project's design and history.
The Python method below was not the visual default. The [browser production
reference](browser-production.md) describes the alternative. Both required a
contact-sheet review before final rendering.

For the historical Python method, the producer supplied `render.py`, scene data,
and numbered `s*.tts.txt` narration files in a task-owned directory. No renderer or
private scenes are bundled. Script inspection and authorized write paths were
required before execution.

The reported renderer used Python 3, Pillow, NumPy, macOS Arial/Arial Unicode
fonts, Samantha, and FFmpeg/FFprobe. It measured WAV narration. Each scene had
0.25 seconds of leading silence and 0.40 seconds of trailing silence. It wrote
`narration.wav` and scene timings. It streamed RGB24 frames at 1280×720 and 30 fps.
These are historical settings, not universal requirements.

Private directories used mode `0700` and files used `0600`. The task record listed
tools, authorized write paths, renderer source, scene inputs, and permissions.

## 2. Narrate and render

The historical sequence ran in the prepared directory and stopped on failure:

```sh
set -e
for f in s*.tts.txt; do say -v Samantha -r 182 -f "$f" -o "${f%.tts.txt}.aiff"; done
for f in s*.aiff; do ffmpeg -loglevel error -y -i "$f" -ar 48000 -ac 1 "${f%.aiff}.wav"; done
python3 render.py
```

The renderer used the following encoder command, with its RGB frames on standard
input. It was not a separate render step:

```sh
ffmpeg -loglevel error -y \
  -f rawvideo -pix_fmt rgb24 -s 1280x720 -r 30 -i - \
  -i narration.wav \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 \
  -shortest -movflags +faststart output.mp4
```

`-y` permits overwrites. The workflow required preserving an accepted copy before
revision. `-shortest` can truncate output if stream lengths differ.

## 3. Check the final file

These commands supported the [final-media checklist](../REFERENCE.md#5-verify-and-deliver):

```sh
shasum -a 256 output.mp4
ffprobe -v error -show_format -show_streams -of json output.mp4
ffmpeg -v error -i output.mp4 -f null -
```

Scene-audio checks used `volumedetect` and `silencedetect=n=-45dB:d=1.5` within
narration windows. Those thresholds are examples. Intentional padding and missing
narration are different states. The record required all main-checklist results
against the final hash, including scene coverage and actual duration.
