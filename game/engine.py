# يدير تقدم اللاعب بين الأحداث


from game.story import load_story
from game.puzzles import load_puzzles
from game.journal import Journal
from game.exploration import Exploration


def play_event(event, journal, puzzles):
    print("\n" + "=" * 45)
    print(f"\n{event['title']}\n")
    print(event["description"])

    choices = event["choices"]

    while True:
        print("\nChoose your action:")

        for index, choice in enumerate(choices, start=1):
            print(f"{index}. {choice['text']}")

        print("J. Review Journal")

        answer = input("\nYour choice: ").strip().lower()

        if answer == "j":
            journal.display()
            continue

        if not answer.isdigit():
            print("Invalid choice. Please try again.")
            continue

        choice_number = int(answer)

        if not 1 <= choice_number <= len(choices):
            print("Invalid choice. Please try again.")
            continue

        selected_choice = choices[choice_number - 1]
        puzzle_id = selected_choice.get("puzzle_id")

        if puzzle_id is not None:
            puzzle_key = str(puzzle_id)

            if puzzle_key not in puzzles:
                print("Error: Puzzle not found.")
                continue

            if not selected_choice.get("correct", False):
                print(f"\n{selected_choice['result']}")
                print(f"Hint: {puzzles[puzzle_key]['hint']}")
                print("Try again.")
                continue

            journal.record_solved_puzzle(puzzle_key)

        evidence = selected_choice.get("evidence")

        if evidence:
            journal.add_evidence(evidence)

        print(f"\n{selected_choice['result']}")
        return selected_choice


def run_game():
    events = load_story()
    puzzles = load_puzzles()
    journal = Journal()
    exploration = Exploration()

    # Connect story events to their IDs.
    events_by_id = {
        event["id"]: event
        for event in events
    }

    print("\n" + "=" * 45)
    print("       ELDERGROVE: THE FORGOTTEN FOREST")
    print("=" * 45)
    print("The forest remembers. Will you escape?")

    input("\nPress Enter to begin...")

    game_finished = False

    while not game_finished:
        exploration.show_locations()

        print("N. Next Region")
        print("J. Review Journal")
        print("Q. Return to Main Menu")

        answer = input("\nSelect an option: ").strip().lower()

        if answer == "j":
            journal.display()
            continue

        if answer == "q":
            print("\nLeaving the forest...")
            break

        if answer == "n":
            exploration.move_to_next_region()
            continue

        if not answer.isdigit():
            print("Invalid option. Please try again.")
            continue

        location_number = int(answer)
        location = exploration.visit_location(location_number)

        if location is None:
            continue

        location_id = location["id"]

        # Allow revisiting without replaying completed events.
        if location_id in exploration.completed_locations:
            print("\nYou have already explored this location.")
            input("\nPress Enter to return...")
            continue

        event_id = location.get("event_id")

        if event_id is not None:
            event = events_by_id.get(event_id)

            if event is None:
                print("Error: Story event not found.")
                continue

            play_event(event, journal, puzzles)

        else:
            print("\nYou explore the area and uncover its secrets.")

        exploration.complete_location(location_id)

        print("\nLocation completed!")

        if location_id == "last_passage":
            game_finished = True
            break

        input("\nPress Enter to continue...")

    if game_finished:
        journal.display()

        print("\n" + "=" * 45)
        print("You have reached the end of the current story.")
        print("=" * 45)
