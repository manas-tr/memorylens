import os
import soundfile as sf
import torch
from dotenv import load_dotenv
from pyannote.audio import Pipeline

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

print("loading diarization pipeline...")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-community-1",
    token=HF_TOKEN,
)

print("loading audio....")

waveform, sample_rate = sf.read("vid01.wav")

if waveform.ndim == 1:
    waveform = waveform[None, :]
else:
    waveform = waveform.T

waveform = torch.from_numpy(waveform).float()

print("processing audio....")

output = pipeline({"waveform": waveform, "sample_rate": sample_rate})
diarization = output.speaker_diarization

print("\nwho spoke when:\n")
for turn, speaker in diarization:
    print(f"{turn.start:.1f}s -> {turn.end:.1f}s : {speaker}")