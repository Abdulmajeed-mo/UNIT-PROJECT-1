
# Manages game progression, story events, scoring, and localization.

from game.story import load_story, localize_story
from game.puzzles import select_random_puzzles, solve_puzzle
from game.journal import Journal
from game.exploration import Exploration
from game.explorers import Explorer, save_explorer_record
from game.scoring import Scoring
from game.save_system import save_game
from game.endings import determine_fate, display_ending
from game.localization import Localization


def game_text(loc, english, arabic):
    """Return text in the selected language."""
    text = arabic if loc.language == "ar" else english
    return loc.format_arabic(text)


def show_forest_memory(event_id, previous_choices, journal, loc):
    """Show how the forest reacts to earlier decisions."""
    messages = []

    if event_id == 4:
        gate_choice = previous_choices.get(1)

        if gate_choice == 3:
            messages = [
                (
                    "The mist whispers with a familiar voice.",
                    "يهمس الضباب بصوت مألوف."
                ),
                (
                    "The forest remembers that you listened at the gate.",
                    "تتذكر الغابة أنك أنصت إلى الهمسات عند البوابة."
                )
            ]

        elif gate_choice == 2:
            messages = [
                (
                    "A faded moon symbol appears through the mist.",
                    "يظهر رمز قمر باهت وسط الضباب."
                ),
                (
                    "The forest remembers your discovery at the gate.",
                    "تتذكر الغابة ما اكتشفته عند البوابة."
                )
            ]

    elif event_id == 6:
        watcher_choice = previous_choices.get(2)

        if watcher_choice == 1:
            messages = [
                (
                    "The stranger knows you spoke honestly to the Watcher.",
                    "يعرف الغريب أنك تحدثت بصدق إلى الحارس."
                )
            ]

        elif watcher_choice == 2:
            messages = [
                (
                    "The stranger watches you with suspicion.",
                    "يراقبك الغريب بريبة."
                ),
                (
                    "Your earlier deception has not been forgotten.",
                    "لم يُنسَ خداعك السابق."
                )
            ]

    elif event_id == 9:
        if "hidden_trials" in journal.discoveries:
            messages.append(
                (
                    "The archway recognizes your understanding of the trials.",
                    "يدرك القوس الحجري أنك فهمت حقيقة الاختبارات."
                )
            )

        if "forest_memory" in journal.discoveries:
            messages.append(
                (
                    "The forest echoes the memories you uncovered.",
                    "تردد الغابة أصداء الذكريات التي اكتشفتها."
                )
            )

    for english, arabic in messages:
        print(f"\n{game_text(loc, english, arabic)}")


def play_event(event, journal, selected_puzzles, scoring, loc):
    """Play a story event without changing its original game data."""
    print("\n" + "=" * 45)

    if loc.language == "ar":
        title = event.get("title_ar", event["title"])
        description = event.get(
            "description_ar", event["description"]
        )
    else:
        title = event["title"]
        description = event["description"]

    print(f"\n{loc.format_arabic(title)}\n")
    print(loc.format_arabic(description))

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
        if not solve_puzzle(
            puzzle_id, selected_puzzles, journal, loc
        ):
            return None

        correct_choice = next(
            (
                choice
                for choice in choices
                if choice.get("correct")
            ),
            None
        )

        if correct_choice is None:
            print(
                game_text(
                    loc,
                    "Error: Correct story choice not found.",
                    "خطأ: لم يتم العثور على الاختيار الصحيح."
                )
            )
            return None

        if journal.record_solved_puzzle(puzzle_id):
            if scoring.add_points("puzzles", puzzle_id, 100):
                print(
                    game_text(
                        loc,
                        "\n+100 Puzzle Points!",
                        "\n+100 نقطة للألغاز!"
                    )
                )

        selected_choice = correct_choice

    else:
        while True:
            print(
                "\n" + game_text(
                    loc,
                    "Choose your action:",
                    "اختر تصرفك:"
                )
            )

            for index, choice in enumerate(choices, start=1):
                if loc.language == "ar":
                    choice_text = choice.get(
                        "text_ar", choice["text"]
                    )
                else:
                    choice_text = choice["text"]

                print(
                    f"{index}. {loc.format_arabic(choice_text)}"
                )

            print(
                f"J. {game_text(loc, 'Review Journal', 'عرض دفتر الرحلة')}"
            )

            prompt = game_text(
                loc,
                "\nYour choice:",
                "\nاختيارك:"
            )
            answer = input(f"{prompt} ").strip().lower()

            if answer == "j":
                journal.display()
                continue

            if not answer.isdigit():
                print(
                    game_text(
                        loc,
                        "Invalid choice. Please try again.",
                        "اختيار غير صحيح، حاول مجددًا."
                    )
                )
                continue

            choice_number = int(answer)

            if not 1 <= choice_number <= len(choices):
                print(
                    game_text(
                        loc,
                        "Invalid choice. Please try again.",
                        "اختيار غير صحيح، حاول مجددًا."
                    )
                )
                continue

            selected_choice = choices[choice_number - 1]
            break

        if scoring.add_points(
            "decisions",
            f"event_{event['id']}",
            40
        ):
            print(
                game_text(
                    loc,
                    "\n+40 Decision Points!",
                    "\n+40 نقطة للقرارات!"
                )
            )

    evidence = selected_choice.get("evidence")

    if evidence and journal.add_evidence(evidence):
        if scoring.add_points("evidence", evidence, 25):
            print(
                game_text(
                    loc,
                    "+25 Evidence Points!",
                    "+25 نقطة للأدلة!"
                )
            )

    if loc.language == "ar":
        result_text = selected_choice.get(
            "result_ar", selected_choice["result"]
        )
    else:
        result_text = selected_choice["result"]

    print(f"\n{loc.format_arabic(result_text)}")

    return selected_choice


def build_game_state(
    explorer,
    exploration,
    journal,
    scoring,
    selected_puzzles,
    previous_choices,
    language
):
    """Build a serializable state for saving the journey."""
    return {
        "language": language,
        "explorer": {
            "name": explorer.name,
            "started_at": explorer.started_at,
            "playtime_seconds": explorer.get_playtime(),
        },
        "exploration": {
            "current_region": exploration.current_region,
            "visited_locations": list(
                exploration.visited_locations
            ),
            "completed_locations": list(
                exploration.completed_locations
            ),
        },
        "journal": {
            "evidence": journal.evidence.copy(),
            "solved_puzzles": journal.solved_puzzles.copy(),
            "discoveries": journal.discoveries.copy(),
        },
        "scoring": {
            "scores": scoring.scores.copy(),
            "rewarded_actions": list(
                scoring.rewarded_actions
            ),
        },
        "selected_puzzles": selected_puzzles,
        "previous_choices": previous_choices.copy(),
    }


def run_game(saved_state=None, language="ar"):
    """Start or resume an explorer's journey."""
    loc = Localization(language)

    if saved_state is not None:
        loc.set_language(
            saved_state.get("language", language)
        )

    events = localize_story(load_story(), loc.language)
    events_by_id = {
        event["id"]: event
        for event in events
    }

    journal = Journal(loc)
    exploration = Exploration()
    scoring = Scoring(loc)

    if saved_state is None:
        selected_puzzles = select_random_puzzles()
        previous_choices = {}

        print("\n" + "=" * 45)
        print(loc.display_text("game_title"))
        print("=" * 45)
        print(loc.display_text("tagline"))

        while True:
            name = input(
                f"\n{loc.display_text('explorer_name')} "
            ).strip()

            if name:
                break

            print(
                game_text(
                    loc,
                    "Explorer name cannot be empty.",
                    "لا يمكن ترك اسم المستكشف فارغًا."
                )
            )

        explorer = Explorer(name)

        print(
            f"\n{loc.display_text('welcome', name=explorer.name)}"
        )

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

        exploration.current_region = exploration_data[
            "current_region"
        ]

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

        journal.discoveries = list(
            journal_data["discoveries"]
        )

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

        welcome = game_text(
            loc,
            "Welcome back",
            "مرحبًا بعودتك"
        )

        started = game_text(
            loc,
            "Journey started",
            "بدأت الرحلة"
        )

        print(
            f"\n{welcome}: {loc.format_arabic(explorer.name)}!"
        )
        print(f"{started}: {explorer.started_at}")

    input(
        game_text(
            loc,
            "\nPress Enter to enter the forest...",
            "\nاضغط Enter لدخول الغابة..."
        )
    )

    game_finished = False
    explorer.start_session()

    try:
        while not game_finished:
            exploration.show_locations(loc)

            print(f"N. {loc.display_text('next_region')}")
            print(f"J. {loc.display_text('journal')}")
            print(f"S. {loc.display_text('view_score')}")
            print(f"T. {loc.display_text('view_playtime')}")
            print(f"V. {loc.display_text('save_option')}")
            print(f"Q. {loc.display_text('return_menu')}")

            answer = input(
                f"\n{loc.display_text('select_location')} "
            ).strip().lower()

            if answer == "j":
                journal.display()
                continue

            if answer == "s":
                scoring.display_score()
                continue

            if answer == "t":
                label = game_text(
                    loc,
                    "Playtime",
                    "مدة اللعب"
                )
                print(
                    f"\n{label}: {explorer.get_duration_text()}"
                )
                continue

            if answer == "v":
                state = build_game_state(
                    explorer,
                    exploration,
                    journal,
                    scoring,
                    selected_puzzles,
                    previous_choices,
                    loc.language
                )

                save_game(state)
                continue

            if answer == "q":
                print(
                    game_text(
                        loc,
                        "\nLeaving the forest...",
                        "\nتغادر الغابة..."
                    )
                )
                break

            if answer == "n":
                exploration.move_to_next_region(loc)
                continue

            if not answer.isdigit():
                print(
                    game_text(
                        loc,
                        "Invalid option. Please try again.",
                        "خيار غير صحيح، حاول مجددًا."
                    )
                )
                continue

            location = exploration.visit_location(
                int(answer), loc
            )

            if location is None:
                continue

            location_id = location["id"]

            if location_id in exploration.completed_locations:
                print(
                    game_text(
                        loc,
                        "\nYou have already explored this location.",
                        "\nلقد استكشفت هذا الموقع مسبقًا."
                    )
                )

                input(
                    game_text(
                        loc,
                        "\nPress Enter to return...",
                        "\nاضغط Enter للعودة..."
                    )
                )
                continue

            event_id = location.get("event_id")

            if event_id is not None:
                event = events_by_id.get(event_id)

                if event is None:
                    print(
                        game_text(
                            loc,
                            "Error: Story event not found.",
                            "خطأ: لم يتم العثور على حدث القصة."
                        )
                    )
                    continue

                show_forest_memory(
                    event_id,
                    previous_choices,
                    journal,
                    loc
                )

                result = play_event(
                    event,
                    journal,
                    selected_puzzles,
                    scoring,
                    loc
                )

                if result is None:
                    print(
                        game_text(
                            loc,
                            "\nThis event could not be completed.",
                            "\nتعذر إكمال هذا الحدث."
                        )
                    )
                    continue

                if event_id not in (3, 5, 7, 8):
                    choice_number = (
                        event["choices"].index(result) + 1
                    )
                    previous_choices[event_id] = choice_number

            else:
                print(
                    game_text(
                        loc,
                        "\nYou explore the area and uncover its secrets.",
                        "\nتستكشف المكان وتكشف أسراره."
                    )
                )
            if location.get("optional", False):
                if scoring.add_points("secrets", location_id, 50):
                    print(
                        game_text(
                            loc,
                            "\n+50 Secret Points!",
                            "\n+50 نقطة للأسرار!"
                        )
                    )
            exploration.complete_location(location_id)

            print(
                game_text(
                    loc,
                    "\nLocation completed!",
                    "\nاكتمل استكشاف الموقع!"
                )
            )

            if location_id == "last_passage":
                game_finished = True
                break

            input(
                game_text(
                    loc,
                    "\nPress Enter to continue...",
                    "\nاضغط Enter للمتابعة..."
                )
            )

    finally:
        explorer.pause_session()

    if game_finished:
        # Choose a random ending from the score's category.
        fate_id = determine_fate(scoring)

        save_explorer_record(
            explorer,
            scoring.get_total(),
            fate_id,
            loc
        )

        display_ending(fate_id, loc)

        print("\n" + "=" * 45)
        print(
            game_text(
                loc,
                "JOURNEY SUMMARY",
                "ملخص الرحلة"
            )
        )
        print("=" * 45)

        explorer_label = game_text(
            loc, "Explorer", "المستكشف"
        )

        started_label = game_text(
            loc, "Journey started", "بدأت الرحلة"
        )

        playtime_label = game_text(
            loc, "Playtime", "مدة اللعب"
        )

        print(
            f"{explorer_label}: "
            f"{loc.format_arabic(explorer.name)}"
        )

        print(
            f"{started_label}: {explorer.started_at}"
        )

        print(
            f"{playtime_label}: "
            f"{explorer.get_duration_text()}"
        )

        scoring.display_score()
        journal.display()

        print(
            game_text(
                loc,
                "\nThe forest will remember your name.",
                "\nستتذكر الغابة اسمك."
            )
        )
