import os
import json

import soundfile as sf
import torch

from dotenv import load_dotenv
from pyannote.audio import Pipeline


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

AUDIO_FILE = "vid01.wav"

OUT_DIR = "outputs"


print("loading diarization pipeline...")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-community-1",
    token=HF_TOKEN
)


print("loading audio...")

waveform, sample_rate = sf.read(
    AUDIO_FILE
)

if waveform.ndim == 1:

    waveform = waveform[None, :]

else:

    waveform = waveform.T


waveform = torch.from_numpy(
    waveform
).float()


print("processing audio...")

output = pipeline(
    {
        "waveform": waveform,
        "sample_rate": sample_rate
    }
)

diarization = output.speaker_diarization


segments = []

for turn, speaker in diarization:

    segments.append({

        "start": round(
            turn.start,
            1
        ),

        "end": round(
            turn.end,
            1
        ),

        "speaker": speaker
    })


os.makedirs(
    OUT_DIR,
    exist_ok=True
)


with open(
    os.path.join(
        OUT_DIR,
        "diarization.json"
    ),
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        segments,
        f,
        indent=2
    )


print(
    "saved outputs/diarization.json"
)