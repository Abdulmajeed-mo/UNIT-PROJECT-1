# يدير تقدم اللاعب بين الأحداث
  

from game.story import load_story
from game.puzzles import select_random_puzzles, solve_puzzle
from game.journal import Journal
from game.exploration import Exploration
from game.explorers import Explorer
from game.scoring import Scoring
from game.save_system import save_game
from game.endings import determine_fate, display_ending
from game.explorers import save_explorer_record


def show_forest_memory(event_id, previous_choices, journal):
    if event_id == 4:
        gate_choice = previous_choices.get(1)

        if gate_choice == 3:
            print("\nThe mist whispers with a familiar voice.")
            print("The forest remembers that you listened at the gate.")
        elif gate_choice == 2:
            print("\nA faded moon symbol appears through the mist.")
            print("The forest remembers your discovery at the gate.")

    elif event_id == 6:
        watcher_choice = previous_choices.get(2)

        if watcher_choice == 1:
            print("\nThe stranger knows you spoke honestly to the Watcher.")
        elif watcher_choice == 2:
            print("\nThe stranger watches you with suspicion.")
            print("Your earlier deception has not been forgotten.")

    elif event_id == 9:
        if "hidden_trials" in journal.discoveries:
            print("\nThe archway recognizes your understanding of the trials.")

        if "forest_memory" in journal.discoveries:
            print("\nThe forest echoes the memories you uncovered.")


def play_event(event, journal, selected_puzzles, scoring):
    print("\n" + "=" * 45)
    print(f"\n{event['title']}\n")
    print(event["description"])

    choices = event["choices"]

    puzzle_id = next(
        (
            str(choice["puzzle_id"])
            for choice in choices
            if "puzzle_id" in choice
        ),
        None
    )

    if puzzle_id is not None:
        if not solve_puzzle(puzzle_id, selected_puzzles, journal):
            return None

        correct_choice = next(
            (choice for choice in choices if choice.get("correct")),
            None
        )

        if correct_choice is None:
            print("Error: Correct story choice not found.")
            return None

        if journal.record_solved_puzzle(puzzle_id):
            if scoring.add_points("puzzles", puzzle_id, 100):
                print("\n+100 Puzzle Points!")

        selected_choice = correct_choice

    else:
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
            break

        if scoring.add_points(
            "decisions",
            f"event_{event['id']}",
            40
        ):
            print("\n+40 Decision Points!")

    evidence = selected_choice.get("evidence")

    if evidence and journal.add_evidence(evidence):
        if scoring.add_points("evidence", evidence, 25):
            print("+25 Evidence Points!")

    print(f"\n{selected_choice['result']}")
    return selected_choice


def build_game_state(
    explorer, exploration, journal, scoring,
    selected_puzzles, previous_choices
):
    return {
        "explorer": {
            "name": explorer.name,
            "started_at": explorer.started_at,
            "playtime_seconds": explorer.get_playtime(),
        },
        "exploration": {
            "current_region": exploration.current_region,
            "visited_locations": list(exploration.visited_locations),
            "completed_locations": list(exploration.completed_locations),
        },
        "journal": {
            "evidence": journal.evidence.copy(),
            "solved_puzzles": journal.solved_puzzles.copy(),
            "discoveries": journal.discoveries.copy(),
        },
        "scoring": {
            "scores": scoring.scores.copy(),
            "rewarded_actions": list(scoring.rewarded_actions),
        },
        "selected_puzzles": selected_puzzles,
        "previous_choices": previous_choices.copy(),
    }


def run_game(saved_state=None):
    events = load_story()
    events_by_id = {event["id"]: event for event in events}

    journal = Journal()
    exploration = Exploration()
    scoring = Scoring()

    if saved_state is None:
        selected_puzzles = select_random_puzzles()
        previous_choices = {}

        print("\n" + "=" * 45)
        print("       ELDERGROVE: THE FORGOTTEN FOREST")
        print("=" * 45)
        print("The forest remembers. Will you escape?")

        while True:
            name = input("\nEnter your explorer name: ").strip()

            if name:
                break

            print("Explorer name cannot be empty.")

        explorer = Explorer(name)
        print(f"\nWelcome to Eldergrove, {explorer.name}!")

    else:
        explorer_data = saved_state["explorer"]
        exploration_data = saved_state["exploration"]
        journal_data = saved_state["journal"]
        scoring_data = saved_state["scoring"]

        explorer = Explorer(explorer_data["name"])
        explorer.started_at = explorer_data["started_at"]
        explorer.playtime_seconds = float(
            explorer_data["playtime_seconds"]
        )

        exploration.current_region = exploration_data["current_region"]
        exploration.visited_locations = set(
            exploration_data["visited_locations"]
        )
        exploration.completed_locations = set(
            exploration_data["completed_locations"]
        )

        journal.evidence = list(journal_data["evidence"])
        journal.solved_puzzles = [
            str(puzzle_id)
            for puzzle_id in journal_data["solved_puzzles"]
        ]
        journal.discoveries = list(journal_data["discoveries"])

        scoring.scores = dict(scoring_data["scores"])
        scoring.rewarded_actions = set(
            scoring_data["rewarded_actions"]
        )

        selected_puzzles = saved_state["selected_puzzles"]

        # JSON stores dictionary keys as strings.
        previous_choices = {
            int(event_id): choice_number
            for event_id, choice_number
            in saved_state["previous_choices"].items()
        }

        print(f"\nWelcome back, {explorer.name}!")
        print(f"Journey started: {explorer.started_at}")

    input("\nPress Enter to enter the forest...")

    game_finished = False
    explorer.start_session()

    try:
        while not game_finished:
            exploration.show_locations()

            print("N. Next Region")
            print("J. Review Journal")
            print("S. View Score")
            print("T. View Playtime")
            print("V. Save Game")
            print("Q. Return to Main Menu")

            answer = input("\nSelect an option: ").strip().lower()

            if answer == "j":
                journal.display()
                continue

            if answer == "s":
                scoring.display_score()
                continue

            if answer == "t":
                print(f"\nPlaytime: {explorer.get_duration_text()}")
                continue

            if answer == "v":
                state = build_game_state(
                    explorer,
                    exploration,
                    journal,
                    scoring,
                    selected_puzzles,
                    previous_choices
                )
                save_game(state)
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

            location = exploration.visit_location(int(answer))

            if location is None:
                continue

            location_id = location["id"]

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

                show_forest_memory(
                    event_id, previous_choices, journal
                )

                result = play_event(
                    event, journal, selected_puzzles, scoring
                )

                if result is None:
                    print("\nThis event could not be completed.")
                    continue

                if event_id not in (3, 5, 7, 8):
                    choice_number = event["choices"].index(result) + 1
                    previous_choices[event_id] = choice_number

            else:
                print("\nYou explore the area and uncover its secrets.")

            exploration.complete_location(location_id)
            print("\nLocation completed!")

            if location_id == "last_passage":
                game_finished = True
                break

            input("\nPress Enter to continue...")

    finally:
        explorer.pause_session()

    if game_finished: #هنا يختار نهايه عشوائيه
        fate_id = determine_fate(scoring)
        save_explorer_record(
            explorer,
            scoring.get_total(),
            fate_id
        )
        display_ending(fate_id)

        print("\n" + "=" * 45)
        print("           JOURNEY SUMMARY")
        print("=" * 45)

        print(f"Explorer: {explorer.name}")
        print(f"Journey started: {explorer.started_at}")
        print(f"Playtime: {explorer.get_duration_text()}")

        scoring.display_score()
        journal.display()

        print("\nThe forest will remember your name.")
