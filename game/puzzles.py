# يحتوي الألغاز والإجابات والتلميحات


import json
import random
from pathlib import Path


PUZZLES_FILE = Path(__file__).parent / "data" / "puzzles.json"


def load_puzzles():
    with PUZZLES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def select_random_puzzles():
    puzzle_bank = load_puzzles()

    selected_puzzles = {}

    for puzzle_id, questions in puzzle_bank.items():
        selected_puzzles[puzzle_id] = random.choice(questions).copy()

    return selected_puzzles


def solve_puzzle(puzzle_id, selected_puzzles, journal=None):
    puzzle = selected_puzzles.get(str(puzzle_id))

    if puzzle is None:
        print(f"Error: Puzzle '{puzzle_id}' not found.")
        return False

    print(f"\n{puzzle['question']}\n")

    for index, option in enumerate(puzzle["options"], start=1):
        print(f"{index}. {option}")

    while True:
        answer = input("\nYour answer (or J for Journal): ").strip()

        if answer.lower() == "j":
            if journal is not None:
                journal.display()
            else:
                print("Journal is unavailable.")
            continue

        if not answer.isdigit():
            print("Please enter a valid option number.")
            continue

        choice_number = int(answer)

        if not 1 <= choice_number <= len(puzzle["options"]):
            print("Invalid option. Try again.")
            continue

        if choice_number == puzzle["correct"]:
            print("\nCorrect! The forest reveals its secret.")
            return True

        print(f"\nHint: {puzzle['hint']}")
        print("Incorrect answer. Try again.")
