# يحدد النهاية حسب إنجازات اللاعب

# Determines the explorer's final fate based on score.

import json
import random
from pathlib import Path
from game.localization import Localization


ENDINGS_FILE = Path(__file__).parent / "data" / "endings.json"

ENDINGS_AR_FILE = Path(__file__).parent / "data" / "endings_ar.json"

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



def get_fate_title(fate_id, loc=None):
    if loc is None:
        loc = Localization("en")

    file_path = (
        ENDINGS_AR_FILE
        if loc.language == "ar"
        else ENDINGS_FILE
    )

    with file_path.open("r", encoding="utf-8") as file:
        endings = json.load(file)

    for category in endings.values():
        if fate_id in category:
            return category[fate_id]["title"]

    return fate_id


def display_ending(fate_id, loc=None):
    if loc is None:
        loc = Localization("en")

    file_path = (
        ENDINGS_AR_FILE
        if loc.language == "ar"
        else ENDINGS_FILE
    )

    with file_path.open("r", encoding="utf-8") as file:
        endings = json.load(file)

    for category in endings.values():
        if fate_id in category:
            fate = category[fate_id]

            print("\n" + "=" * 50)
            print(loc.format_arabic(fate["title"]))
            print("=" * 50)

            print(
                f"\n{loc.format_arabic(fate['description'])}"
            )

            message = (
                "الغابة تتذكر رحلتك."
                if loc.language == "ar"
                else "The forest remembers your journey."
            )

            print(f"\n{loc.format_arabic(message)}")
            return

    message = (
        "مصير غير معروف."
        if loc.language == "ar"
        else "Unknown fate."
    )
    print(f"\n{loc.format_arabic(message)}")

