# أسماء المستكشفين وسجلات رحلاتهم مع الوقت 

import json
from pathlib import Path
from datetime import datetime
from time import monotonic


class Explorer:
    def __init__(self, name):
        self.name = name.strip()
        self.started_at = datetime.now().isoformat(timespec="seconds")
        self.playtime_seconds = 0.0
        self.session_started = None

    def start_session(self):
        if self.session_started is None:
            self.session_started = monotonic()

    def pause_session(self):
        if self.session_started is not None:
            self.playtime_seconds += monotonic() - self.session_started
            self.session_started = None

    def get_playtime(self):
        total = self.playtime_seconds

        if self.session_started is not None:
            total += monotonic() - self.session_started

        return int(total)

    def get_duration_text(self):
        seconds = self.get_playtime()
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours:02}:{minutes:02}:{seconds:02}"


RECORDS_FILE = (
    Path(__file__).resolve().parent.parent
    / "records"
    / "explorers.json"
)


def load_explorer_records():
    if not RECORDS_FILE.exists():
        return []

    try:
        with RECORDS_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError("Invalid explorer records.")

        return records

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Could not load explorer records: {error}")
        return None


def save_explorer_record(explorer, score, fate_id):
    records = load_explorer_records()

    if records is None:
        return False

    record = {
        "name": explorer.name,
        "started_at": explorer.started_at,
        "score": score,
        "duration_seconds": explorer.get_playtime(),
        "fate": fate_id,
    }

    # Prevent recording the same journey twice.
    if any(
        item["name"] == record["name"]
        and item["started_at"] == record["started_at"]
        for item in records
    ):
        return False

    records.append(record)

    records.sort(
        key=lambda item: (
            -item["score"],
            item["duration_seconds"]
        )
    )

    try:
        RECORDS_FILE.parent.mkdir(parents=True, exist_ok=True)

        temporary_file = RECORDS_FILE.with_suffix(".tmp")

        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, ensure_ascii=False)

        temporary_file.replace(RECORDS_FILE)

        print("\nYour journey has been recorded in the Hall!")
        return True

    except OSError as error:
        print(f"Could not save explorer record: {error}")
        return False


def display_hall():
    records = load_explorer_records()

    print("\n" + "=" * 60)
    print("              HALL OF LOST EXPLORERS")
    print("=" * 60)

    if not records:
        print("No explorer journeys recorded yet.")
        return

    for rank, record in enumerate(records, start=1):
        minutes, seconds = divmod(record["duration_seconds"], 60)

        print(f"\n{rank}. {record['name']}")
        print(f"   Score: {record['score']}/1000")
        print(f"   Time: {minutes:02}:{seconds:02}")
        print(f"   Date: {record['started_at']}")
        print(f"   Fate: {record['fate']}")

    print("\n" + "=" * 60)
