# Historical Local Kokoro Voice Recipe

> **Unmaintained snapshot.** For study only. The [snapshot warning and source record](../REFERENCE.md) apply to this file. Dependencies and commands are historical, not a current installation recommendation.

The source used local Kokoro as its default narration voice. The producer supplied
narration, scene timings, and a renderer. No renderer or private scenes are bundled.

## 1. Prepare the local environment

The historical setup used a task-local scratch directory outside Git. It pinned
Kokoro and the English language model, not every dependency. The resolved
dependency list (`uv pip freeze`) was saved with the editable media source.

```sh
umask 077
mkdir -p .local-voice/cache
export UV_CACHE_DIR="$PWD/.local-voice/cache/uv"
uv venv .local-voice/venv --python 3.11
# On Linux without a GPU, install the CPU wheel first.
uv pip install --python .local-voice/venv/bin/python torch \
  --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .local-voice/venv/bin/python \
  'kokoro==0.9.4' soundfile pillow espeakng-loader
uv pip install --python .local-voice/venv/bin/python \
  https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
export HF_HOME="$PWD/.local-voice/cache/huggingface"
export HF_HUB_DISABLE_IMPLICIT_TOKEN=1
export HF_HUB_DISABLE_TELEMETRY=1
export PYTHONDONTWRITEBYTECODE=1
```

Espeak's library and data came through `espeakng-loader`, without a system Espeak
installation. The task record listed the interpreter, packages, and cache paths.

## 2. Download public assets

The excerpts used the local interpreter. The public model download required no
authentication token:

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

Configuration, model weights, and the voice tensor had to exist in the pinned
local snapshot before generation.

## 3. Generate offline narration

The historical defaults were CPU, voice `af_heart`, and speed `1.1`. Offline mode
was set after the download and before generation:

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

Each sentence had one clip. In this excerpt, `text` is its approved spoken form;
each clip needs a separate file name:

```python
chunks = [audio.numpy() for _, _, audio in pipeline(text, voice=voice, speed=1.1)]
audio = np.concatenate(chunks)
assert len(audio) > 0 and np.isfinite(audio).all()
sf.write("clip.24k.wav", audio, 24000, subtype="PCM_16")
```

```sh
ffmpeg -loglevel error -y -i clip.24k.wav -ar 48000 -ac 1 -c:a pcm_s16le clip.wav
```

The clip manifest recorded file names, measured durations, and SHA-256 hashes of
spoken text. A rerun kept unchanged clips and generated new or changed sentences.
The timing builder rejected clips whose hashes differed from current text.
Captions and spoken text could differ for pronunciation; both stayed in the scene
source, and the spoken form was hashed.

The required output was finite, nonempty 48 kHz mono PCM audio for every sentence,
generated locally without network access.

## 4. Render the scenes

The new timing manifest used measured clip durations. The historical renderer
added 0.65 seconds of scene padding.

For an approved replacement, the original media was preserved. The renderer
sampled each original scene at `original_time = new_time ×
original_scene_duration / new_scene_duration`. This mapped the playback clock,
not an old reveal timestamp.

The supplied renderer used the new clips, timings, and diagrams and wrote a
distinct intermediate file, such as `rendered.mp4`. There is no bundled render
command. A renderer that cannot use those inputs is a blocker.

## 5. Normalize the audio

The historical target was −16 LUFS integrated and −1.5 dBTP. This two-pass pattern
could be applied to mixed narration before encoding or to an intermediate video.
The parser requires FFmpeg's newline-plus-opening-brace marker.
`JSONDecoder.raw_decode` permits trailing progress text.

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

The expected result was `normalized.mp4` with copied video and normalized AAC
audio. Encoding success did not replace final-media checks.

## 6. Check the encoded result

The source required the [final-media checklist](../REFERENCE.md#5-verify-and-deliver)
against the encoded file's hash. Checks included clipped syllables, distortion,
and pumping. Loudness and true peak were measured again after AAC encoding. The
final peak can exceed the filter target. Measured values, not requested settings,
were reported. A failed strict ceiling required an audio adjustment and new checks.
