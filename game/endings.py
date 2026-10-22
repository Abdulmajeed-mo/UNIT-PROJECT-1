# يحدد النهاية حسب إنجازات اللاعب

# Determines the explorer's final fate based on score.

import json
import random
from pathlib import Path


ENDINGS_FILE = Path(__file__).parent / "data" / "endings.json"

PASSING_SCORE = 600


def load_endings():
    with ENDINGS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def determine_fate(scoring):
    endings = load_endings()
    total_score = scoring.get_total()

    if total_score >= PASSING_SCORE:
        category = "positive"
    else:
        category = "negative"

    possible_fates = list(endings[category].keys())

    fate_id = random.choice(possible_fates)

    return fate_id


def display_ending(fate_id):
    endings = load_endings()

    for category in endings.values():
        if fate_id in category:
            fate = category[fate_id]

            print("\n" + "=" * 50)
            print(f"               {fate['title']}")
            print("=" * 50)

            print(f"\n{fate['description']}")
            print("\nThe forest remembers your journey.")

            return

    print("\nUnknown fate.")
