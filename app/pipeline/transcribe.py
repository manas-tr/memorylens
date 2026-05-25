import os
import json
import whisper


VIDEO_FILE = "vid01.mp4"

OUT_DIR = "outputs"


print("loading model...")

model = whisper.load_model("base")


print("transcribing...")

result = model.transcribe(
    VIDEO_FILE,
    fp16=False
)


segments = []

for seg in result["segments"]:

    segments.append({

        "start": round(
            seg["start"],
            1
        ),

        "end": round(
            seg["end"],
            1
        ),

        "text": seg["text"].strip()
    })


os.makedirs(
    OUT_DIR,
    exist_ok=True
)


with open(
    os.path.join(
        OUT_DIR,
        "transcript.json"
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
    "saved outputs/transcript.json"
)