import json


MEMORY_FILE = "outputs/memory_timeline.json"


with open(
    MEMORY_FILE,
    "r",
    encoding="utf-8"
) as f:

    memory = json.load(f)


print("\nsearch memory\n")


query = input(
    "search: "
).lower().strip()


print()


found = False


for entry in memory:

    text = entry["text"].lower()

    person = entry["person"].lower()

    visible = " ".join(
        entry["visible"]
    ).lower()

    speaker = entry["speaker"].lower()


    if (
        query in text
        or query in person
        or query in visible
        or query in speaker
    ):

        found = True

        print(
            f"[{entry['start']}s -> {entry['end']}s]"
        )

        print(
            f"speaker : {entry['speaker']}"
        )

        print(
            f"person  : {entry['person']}"
        )

        print(
            f"visible : {entry['visible']}"
        )

        print(
            f"text    : {entry['text']}"
        )

        print()


if not found:

    print("nothing found")