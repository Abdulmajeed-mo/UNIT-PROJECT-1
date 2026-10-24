# يحتوي الألغاز والإجابات والتلميحات


# Handles randomized puzzles, answers, hints, and localization.

import json
import random
from pathlib import Path

from game.localization import Localization


DATA_DIR = Path(__file__).parent / "data"
PUZZLES_FILE = DATA_DIR / "puzzles.json"
PUZZLES_AR_FILE = DATA_DIR / "puzzles_ar.json"


def load_puzzles():
    with PUZZLES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_arabic_puzzles():
    with PUZZLES_AR_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def select_random_puzzles():
    puzzle_bank = load_puzzles()
    selected_puzzles = {}

    for puzzle_id, questions in puzzle_bank.items():
        selected_index = random.randrange(len(questions))
        selected_puzzles[puzzle_id] = questions[selected_index].copy()

        # Save the index so the same question can be translated
        # even after the player saves and resumes the game.
        selected_puzzles[puzzle_id]["question_index"] = selected_index

    return selected_puzzles


def solve_puzzle(
    puzzle_id, selected_puzzles, journal=None, loc=None
):
    if loc is None:
        loc = Localization("en")

    puzzle_id = str(puzzle_id)
    puzzle = selected_puzzles.get(puzzle_id)

    if puzzle is None:
        print(f"Error: Puzzle '{puzzle_id}' not found.")
        return False

    question = puzzle["question"]
    options = puzzle["options"]
    hint = puzzle["hint"]

    if loc.language == "ar":
        arabic_bank = load_arabic_puzzles()
        question_index = puzzle.get("question_index")

        # Support older save files that have no question_index.
        if question_index is None:
            original_questions = load_puzzles().get(puzzle_id, [])

            for index, original in enumerate(original_questions):
                if original["question"] == puzzle["question"]:
                    question_index = index
                    break

        arabic_questions = arabic_bank.get(puzzle_id, [])

        if (
            question_index is not None
            and 0 <= question_index < len(arabic_questions)
        ):
            translated = arabic_questions[question_index]
            question = translated["question"]
            options = translated["options"]
            hint = translated["hint"]

    print(f"\n{loc.format_arabic(question)}\n")

    for index, option in enumerate(options, start=1):
        print(f"{index}. {loc.format_arabic(option)}")

    while True:
        answer_prompt = (
            "إجابتك (أو J لفتح دفتر الرحلة):"
            if loc.language == "ar"
            else "Your answer (or J for Journal):"
        )

        answer = input(
            f"\n{loc.format_arabic(answer_prompt)} "
        ).strip().lower()

        if answer == "j":
            if journal is not None:
                journal.display()
            else:
                message = (
                    "دفتر الرحلة غير متاح."
                    if loc.language == "ar"
                    else "Journal is unavailable."
                )
                print(loc.format_arabic(message))
            continue

        if not answer.isdigit():
            message = (
                "أدخل رقم خيار صحيح."
                if loc.language == "ar"
                else "Please enter a valid option number."
            )
            print(loc.format_arabic(message))
            continue

        choice_number = int(answer)

        if not 1 <= choice_number <= len(options):
            message = (
                "خيار غير صحيح، حاول مجددًا."
                if loc.language == "ar"
                else "Invalid option. Try again."
            )
            print(loc.format_arabic(message))
            continue

        # Always check the original English puzzle's answer.
        if choice_number == puzzle["correct"]:
            message = (
                "إجابة صحيحة! تكشف الغابة أحد أسرارها."
                if loc.language == "ar"
                else "Correct! The forest reveals its secret."
            )
            print(f"\n{loc.format_arabic(message)}")
            return True

        hint_label = "تلميح" if loc.language == "ar" else "Hint"
        print(
            f"\n{loc.format_arabic(hint_label)}: "
            f"{loc.format_arabic(hint)}"
        )

        message = (
            "إجابة خاطئة، حاول مجددًا."
            if loc.language == "ar"
            else "Incorrect answer. Try again."
        )
        print(loc.format_arabic(message))
