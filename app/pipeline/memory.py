import os
import json


OUT_DIR = "outputs"


def infer_person(
    start,
    end,
    face_timeline
):

    counts = {}

    for entry in face_timeline:

        t = entry["time"]

        if start <= t <= end:

            for face in entry["visible"]:

                counts[face] = (
                    counts.get(face, 0) + 1
                )

    if not counts:
        return "UNKNOWN"

    best = max(
        counts,
        key=counts.get
    )

    return best


def collect_visible(
    start,
    end,
    face_timeline
):

    visible = []

    for entry in face_timeline:

        t = entry["time"]

        if start <= t <= end:

            visible.extend(
                entry["visible"]
            )

    return sorted(
        list(set(visible))
    )


def best_speaker(
    start,
    end,
    diarization
):

    best = "UNKNOWN"

    best_overlap = 0

    for seg in diarization:

        overlap = max(
            0,
            min(end, seg["end"])
            - max(start, seg["start"])
        )

        if overlap > best_overlap:

            best_overlap = overlap

            best = seg["speaker"]

    return best


def main():

    with open(
        os.path.join(
            OUT_DIR,
            "transcript.json"
        ),
        "r",
        encoding="utf-8"
    ) as f:

        transcript = json.load(f)


    with open(
        os.path.join(
            OUT_DIR,
            "diarization.json"
        ),
        "r",
        encoding="utf-8"
    ) as f:

        diarization = json.load(f)


    with open(
        os.path.join(
            OUT_DIR,
            "face_timeline.json"
        ),
        "r",
        encoding="utf-8"
    ) as f:

        face_timeline = json.load(f)


    print("\nmemory timeline:\n")

    memory = []

    for seg in transcript:

        start = seg["start"]

        end = seg["end"]

        text = seg["text"]


        speaker = best_speaker(
            start,
            end,
            diarization
        )


        person = infer_person(
            start,
            end,
            face_timeline
        )


        visible = collect_visible(
            start,
            end,
            face_timeline
        )


        entry = {

            "start": start,

            "end": end,

            "speaker": speaker,

            "person": person,

            "visible": visible,

            "text": text
        }

        memory.append(entry)

        print(f"[{start}s -> {end}s]")

        print(f"  speaker : {speaker}")

        print(f"  person  : {person}")

        print(f"  visible : {visible}")

        print(f"  text    : {text}")

        print()


    with open(
        os.path.join(
            OUT_DIR,
            "memory_timeline.json"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memory,
            f,
            indent=2
        )

    print(
        "saved outputs/memory_timeline.json"
    )
    
if __name__ == "__main__":
    main()