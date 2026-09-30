# Local Kokoro Voice Option

Use with approval for local voice generation, task-local dependencies, and public model downloads. Follow the main skill's permission and final-media checks.

The examples use public APIs and generic names. The actor is the Tycho producer during production or Amp during an authorized replacement. That actor supplies narration, scene timings, and a renderer. This skill includes no renderer or private scenes.

## 1. Prepare the local environment

Run in an authorized task directory. The installation pins Kokoro and the English language model, not every dependency. Retain a resolved dependency lock.

```sh
umask 077
mkdir -p .local-voice/cache
export UV_CACHE_DIR="$PWD/.local-voice/cache/uv"
uv venv .local-voice/venv --python 3.11
uv pip install --python .local-voice/venv/bin/python \
  'kokoro==0.9.4' soundfile pillow espeakng-loader
uv pip install --python .local-voice/venv/bin/python \
  https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
export HF_HOME="$PWD/.local-voice/cache/huggingface"
export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
export HF_HUB_DISABLE_TELEMETRY=1
export PYTHONDONTWRITEBYTECODE=1
```

Load Espeak's library and data through `espeakng-loader`. This avoids a system Espeak installation.

**Complete when:** the task record lists the local interpreter, required packages, cache paths, and resolved dependency lock.

## 2. Download public assets

Use the local interpreter for these excerpts. Download the public model without an authentication token:

```python
from pathlib import Path
from huggingface_hub import snapshot_download

repo = "hexgrad/Kokoro-82M"
snapshot = Path(snapshot_download(
    repo,
    revision="f3ff3571791e39611d31c381e3a41a3af07b4987",
    token=False,
    allow_patterns=["config.json", "kokoro-v1_0.pth", "voices/af_heart.pt"],
))
```

**Complete when:** configuration, model weights, and voice tensor exist in the pinned local snapshot.

## 3. Generate offline narration

Set offline mode before generation. The tested settings were CPU, `af_heart`, and speed `1.16`:

```sh
export HF_HUB_OFFLINE=1
```

```python
import os
import espeakng_loader
import numpy as np
import soundfile as sf
import torch
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from kokoro import KModel, KPipeline

os.environ["ESPEAK_DATA_PATH"] = espeakng_loader.get_data_path()
EspeakWrapper.set_library(espeakng_loader.get_library_path())
torch.set_num_threads(4)
model = KModel(
    repo_id=repo,
    config=str(snapshot / "config.json"),
    model=str(snapshot / "kokoro-v1_0.pth"),
)
pipeline = KPipeline(lang_code="a", repo_id=repo, model=model, device="cpu")
voice = torch.load(snapshot / "voices/af_heart.pt", map_location="cpu", weights_only=True)
```

For each scene, `text` is its approved narration. Use a separate file name per scene. Keep narration generation local.

```python
chunks = [audio.numpy() for _, _, audio in pipeline(text, voice=voice, speed=1.16)]
audio = np.concatenate(chunks)
assert len(audio) > 0 and np.isfinite(audio).all()
sf.write("clip.24k.wav", audio, 24000, subtype="PCM_16")
```

```sh
ffmpeg -loglevel error -y -i clip.24k.wav -ar 48000 -ac 1 -c:a pcm_s16le clip.wav
```

**Complete when:** local generation produced finite, nonempty 48 kHz mono PCM audio for every scene without network access.

## 4. Render the scenes

Measure clip durations for the new timing manifest. The tested renderer added 0.65 seconds of scene padding.

For a replacement, preserve the original media. Reuse its diagrams through the scene-specific renderer. At each new scene-relative playback time, sample the original renderer at `original_time = new_time × original_scene_duration / new_scene_duration`. This maps the playback clock, not an old reveal timestamp.

Run the supplied renderer with the new clips, new timings, and diagrams. Write a distinct intermediate video such as `rendered.mp4`. There is no bundled render command; inspect the supplied script's interface. Stop if the renderer cannot use the required inputs.

**Complete when:** the intermediate video contains every new narration clip and scene, with a saved timing manifest.

## 5. Normalize the audio

Use this two-pass pattern on the intermediate video. Inspect the measurement output. This parser requires FFmpeg's newline-plus-opening-brace marker. `JSONDecoder.raw_decode` permits trailing progress text, which caused `json.loads` to fail in the source run.

```python
import json
import subprocess

target = "loudnorm=I=-16:TP=-1.5:LRA=7"
stderr = subprocess.run([
    "ffmpeg", "-hide_banner", "-i", "rendered.mp4", "-vn",
    "-af", target + ":print_format=json", "-f", "null", "-",
], check=True, capture_output=True, text=True).stderr
levels, _ = json.JSONDecoder().raw_decode(stderr[stderr.rfind("\n{"):].lstrip())
options = ":".join([
    target,
    f"measured_I={levels['input_i']}",
    f"measured_TP={levels['input_tp']}",
    f"measured_LRA={levels['input_lra']}",
    f"measured_thresh={levels['input_thresh']}",
    f"offset={levels['target_offset']}",
    "linear=true",
])
subprocess.run([
    "ffmpeg", "-loglevel", "error", "-y", "-i", "rendered.mp4",
    "-c:v", "copy", "-af", options,
    "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
    "-movflags", "+faststart", "normalized.mp4",
], check=True)
```

**Complete when:** measurement parsing and encoding succeed, producing `normalized.mp4` with copied video and normalized AAC audio.

## 6. Check the encoded result

Apply the [final-media checklist](../SKILL.md#5-amp-verifies-and-delivers) to `normalized.mp4`. Check for clipped syllables, distortion, and pumping. Remeasure integrated loudness and true peak after AAC encoding. The final peak can exceed the filter target. Report measured values, not requested settings. If a strict ceiling fails, adjust the audio. Then repeat the checks.

**Complete when:** Amp's record contains every main-checklist result and final loudness measurement against the encoded file's hash.
