# يحتوي القصة والأحداث التسعة


import json
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "story.json"


def load_story():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data["events"]
