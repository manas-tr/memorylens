# MemoryLens

> multimodal memory retrieval from videos. built it because i wanted to search through a video like a brain would.

---

so basically — you give it a video, it figures out **who said what, when, and who was visible on screen**, then lets you search through it all in a timeline.

no fancy vector DBs. no LLMs in the loop. just audio + vision + time, fused into something you can actually query.

---

## what it does

```
audio  ──┐
          ├──► memory timeline ──► search
vision ──┘
```

- transcribes speech (whisper)
- figures out who's speaking (pyannote diarization)
- tracks faces and matches identities across frames
- fuses all of it into timestamped memory entries
- lets you search through it via a streamlit UI

---

## pipeline

```
video
│
├── extract_audio.py       →  vid01.wav
├── transcribe.py          →  transcript.json
├── diarize.py             →  diarization.json
├── match_faces.py         →  face_timeline.json
└── memory.py              →  memory_timeline.json
```

each script does one thing. outputs are plain JSON. nothing clever, just readable.

---

## memory entry (what it actually outputs)

```json
{
  "start": 7.0,
  "end": 9.0,
  "speaker": "SPEAKER_00",
  "person": "face_1",
  "visible": ["face_0", "face_1"],
  "text": "Here you go, you can have it."
}
```

that's it. timestamp, who spoke, who's on screen, what was said.

---

## project structure

```
memorylens/
│
├── app/
│   ├── pipeline/
│   │   ├── extract_audio.py
│   │   ├── transcribe.py
│   │   ├── diarize.py
│   │   ├── match_faces.py
│   │   ├── memory.py
│   │   └── retrieval.py
│   │
│   └── ui/
│       └── app.py
│
├── outputs/
├── faces/
├── requirements.txt
└── .gitignore
```

---

## run it

```bash
# 1. pull audio out of the video
python app/pipeline/extract_audio.py

# 2. transcribe it
python app/pipeline/transcribe.py

# 3. diarize (who's speaking when)
python app/pipeline/diarize.py

# 4. track faces + match identities
python app/pipeline/match_faces.py

# 5. fuse everything into memory
python app/pipeline/memory.py

# 6. search from terminal
python app/pipeline/retrieval.py

# 7. or just use the UI
streamlit run app/ui/app.py
```

---

## retrieval

search `face_0` and you get back every moment that person was on screen — what was said, by whom, when.

```
search: face_0

→ timestamps
→ transcript segments
→ speaker clusters
→ visible identities
→ inferred conversational identity
```

---

## stack

| thing     | what for                  |
| --------- | ------------------------- |
| Python    | everything                |
| Whisper   | speech → text             |
| pyannote  | speaker diarization       |
| OpenCV    | face detection + tracking |
| Streamlit | search UI                 |
| JSON      | pipeline glue             |

---

## honest notes

goal wasn't perfect speaker identification. it's a coherent, searchable memory system built on top of raw audio/visual signals — modular, readable, and actually usable.

built it to understand how multimodal fusion works at the pipeline level, not just in a paper.

---
