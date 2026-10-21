# يحتوي الألغاز والإجابات والتلميحات


# Contains puzzle questions, answers, and hints.

import json
from pathlib import Path

PUZZLES_FILE = Path(__file__).parent / "data" / "puzzles.json"


def load_puzzles():
    with PUZZLES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)



def solve_puzzle(puzzle_id):
    puzzles = load_puzzles()
    puzzle = puzzles.get(str(puzzle_id))

    if puzzle is None:
        print(f"Error: Puzzle '{puzzle_id}' not found.")
        return False

    print(f"\n{puzzle['question']}")

    while True:
        answer = input("Your answer: ").strip().lower()

        if answer == puzzle["answer"].strip().lower():
            print("Correct! The forest reveals its secret.")
            return True

        print(f"Hint: {puzzle['hint']}")
        print("Incorrect answer. Try again.")
