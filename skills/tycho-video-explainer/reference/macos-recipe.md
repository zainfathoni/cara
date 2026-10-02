# Local macOS Recipe

Use on an authorized macOS host with the required tools installed. Follow the main skill's permission and final-media checks.

## 1. Prepare the renderer

Use the renderer selected under the main skill's design and history checks. The Python method below records an earlier run; it is not the visual default. For a browser renderer, read the [browser production reference](browser-production.md) and use that renderer's interface with the generated speech. Complete the main skill's contact-sheet gate before final rendering with either method.

For the recorded Python method, the producer supplies `render.py`, scene data, and numbered `s*.tts.txt` narration files in a task-owned directory. This skill includes no renderer or private scenes. Inspect the script before execution. Require writes to remain within authorized locations.

The tested renderer used Python 3, Pillow, NumPy, macOS Arial/Arial Unicode fonts, Samantha, and FFmpeg/FFprobe. It measured WAV narration. Each scene had 0.25 seconds of leading silence and 0.40 seconds of trailing silence. It wrote `narration.wav` and scene timings. It streamed RGB24 frames at 1280×720 and 30 fps. These are example settings, not universal requirements.

Restrict private directories to `0700` and files to `0600`.

**Complete when:** the producer's record confirms tools, authorized write paths, renderer source, scene inputs, and file permissions.

## 2. Narrate and render

Run in the prepared directory. Stop on a command failure. This is the tested sequence:

```sh
set -e
for f in s*.tts.txt; do say -v Samantha -r 182 -f "$f" -o "${f%.tts.txt}.aiff"; done
for f in s*.aiff; do ffmpeg -loglevel error -y -i "$f" -ar 48000 -ac 1 "${f%.aiff}.wav"; done
python3 render.py
```

The renderer used the following encoder command. Select an authorized path instead of the generic `output.mp4` name. Run this command inside the renderer with its RGB frames on standard input. It is not a separate rendering step.

```sh
ffmpeg -loglevel error -y \
  -f rawvideo -pix_fmt rgb24 -s 1280x720 -r 30 -i - \
  -i narration.wav \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 \
  -shortest -movflags +faststart output.mp4
```

`-y` permits overwrites. Preserve an accepted copy before revision. `-shortest` can truncate output if stream lengths differ.

**Complete when:** the producer has every narration clip, combined audio, scene timings, and encoded video, and all commands succeeded.

## 3. Check the final file

Apply the [final-media checklist](../SKILL.md#5-amp-verifies-and-delivers). These commands support its hash, metadata, and full-decode checks:

```sh
shasum -a 256 output.mp4
ffprobe -v error -show_format -show_streams -of json output.mp4
ffmpeg -v error -i output.mp4 -f null -
```

For scene-audio checks, the tested method used `volumedetect` and `silencedetect=n=-45dB:d=1.5` within narration windows. These thresholds are examples. Distinguish intentional padding from missing narration.

**Complete when:** Amp's record contains every main-checklist result against the final hash, including scene coverage and actual duration.
