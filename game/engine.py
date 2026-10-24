# Eldergrove - The Forgotten Forest
# Game engine: story, exploration, choices, scoring, saving,
# animations, localization, and sound effects.

import questionary

from rich.panel import Panel
from rich.text import Text

from game.story import load_story, localize_story
from game.puzzles import select_random_puzzles, solve_puzzle
from game.journal import Journal
from game.exploration import Exploration
from game.explorers import Explorer, save_explorer_record
from game.scoring import Scoring
from game.save_system import save_game
from game.endings import determine_fate, display_ending
from game.localization import Localization

from ui.effects import (
    console,
    show_forest_entry,
    show_magic_loading,
    show_secret_discovery,
    show_final_fate,
    type_narration,
)

from ui.audio import (
    play_forest,
    play_sound,
    stop_all_audio,
)


# --------------------------------------------------
# Forest Theme
# --------------------------------------------------

FOREST_GREEN = "#2F5249"
ANTIQUE_GOLD = "#C5A46D"
SOFT_GREEN = "#A3B18A"


MENU_STYLE = questionary.Style([
    ("question", "fg:#C5A46D bold"),
    ("pointer", "fg:#C5A46D bold"),
    ("highlighted", "fg:#A3B18A bold"),
    ("selected", "fg:#2F5249"),
    ("disabled", "fg:#858585"),
])


# --------------------------------------------------
# Localization Helpers
# --------------------------------------------------

def game_text(loc, english, arabic):
    """Return formatted text in the selected language."""

    text = arabic if loc.language == "ar" else english
    return loc.format_arabic(text)


def narration(text, loc):
    """Display narration using the typing effect."""

    console.print()

    type_narration(
        text,
        delay=0.035,
        style=SOFT_GREEN,
        formatter=loc.format_arabic,
    )


# --------------------------------------------------
# Exploration Menu
# --------------------------------------------------

def choose_exploration_action(exploration, loc):
    """Select locations and commands using arrow keys."""

    choices = []

    for index, location in enumerate(
        exploration.get_locations(),
        start=1,
    ):
        name = exploration.translate_location(
            location["name"],
            loc,
        )

        completed = (
            location["id"]
            in exploration.completed_locations
        )

        unlocked = exploration.is_unlocked(location)

        if completed:
            icon = "✅"
            status = loc.display_text("completed")

        elif unlocked:
            icon = "🌿"
            status = loc.display_text("available")

        else:
            icon = "🔒"
            status = loc.display_text("locked")

        choices.append(
            questionary.Choice(
                title=f"{icon} {name} [{status}]",
                value=str(index),
                disabled=(
                    status if not unlocked else None
                ),
            )
        )

    choices.extend([
        questionary.Choice(
            title=f"🌳 {loc.display_text('next_region')}",
            value="n",
        ),
        questionary.Choice(
            title=f"📜 {loc.display_text('journal')}",
            value="j",
        ),
        questionary.Choice(
            title=f"🏆 {loc.display_text('view_score')}",
            value="s",
        ),
        questionary.Choice(
            title=f"⏳ {loc.display_text('view_playtime')}",
            value="t",
        ),
        questionary.Choice(
            title=f"💾 {loc.display_text('save_option')}",
            value="v",
        ),
        questionary.Choice(
            title=f"🚪 {loc.display_text('return_menu')}",
            value="q",
        ),
    ])

    return questionary.select(
        loc.display_text("select_location"),
        choices=choices,
        pointer="❯",
        style=MENU_STYLE,
        use_shortcuts=False,
    ).ask()


# --------------------------------------------------
# Forest Memory
# --------------------------------------------------

def show_forest_memory(
    event_id,
    previous_choices,
    journal,
    loc,
):
    """React to earlier decisions and discoveries."""

    messages = []

    if event_id == 4:
        gate_choice = previous_choices.get(1)

        if gate_choice == 3:
            messages = [
                (
                    "The mist whispers with a familiar voice.",
                    "يهمس الضباب بصوت مألوف.",
                ),
                (
                    "The forest remembers that you listened at the gate.",
                    "تتذكر الغابة أنك أنصت إلى الهمسات عند البوابة.",
                ),
            ]

        elif gate_choice == 2:
            messages = [
                (
                    "A faded moon symbol appears through the mist.",
                    "يظهر رمز قمر باهت وسط الضباب.",
                ),
                (
                    "The forest remembers your discovery at the gate.",
                    "تتذكر الغابة ما اكتشفته عند البوابة.",
                ),
            ]

    elif event_id == 6:
        watcher_choice = previous_choices.get(2)

        if watcher_choice == 1:
            messages = [
                (
                    "The stranger knows you spoke honestly to the Watcher.",
                    "يعرف الغريب أنك تحدثت بصدق إلى الحارس.",
                ),
            ]

        elif watcher_choice == 2:
            messages = [
                (
                    "The stranger watches you with suspicion.",
                    "يراقبك الغريب بريبة.",
                ),
                (
                    "Your earlier deception has not been forgotten.",
                    "لم يُنسَ خداعك السابق.",
                ),
            ]

    elif event_id == 9:
        if "hidden_trials" in journal.discoveries:
            messages.append(
                (
                    "The archway recognizes your understanding of the trials.",
                    "يدرك القوس الحجري أنك فهمت حقيقة الاختبارات.",
                )
            )

        if "forest_memory" in journal.discoveries:
            messages.append(
                (
                    "The forest echoes the memories you uncovered.",
                    "تردد الغابة أصداء الذكريات التي اكتشفتها.",
                )
            )

    for english, arabic in messages:
        console.print(
            Text(
                f"🌫️ {game_text(loc, english, arabic)}",
                style=SOFT_GREEN,
            )
        )


# --------------------------------------------------
# Story Events
# --------------------------------------------------

def play_event(
    event,
    journal,
    selected_puzzles,
    scoring,
    loc,
):
    """Run a story event with interactive choices."""

    if loc.language == "ar":
        title = event.get(
            "title_ar",
            event["title"],
        )

        description = event.get(
            "description_ar",
            event["description"],
        )

    else:
        title = event["title"]
        description = event["description"]

    console.print()

    console.print(
        Panel(
            Text(
                loc.format_arabic(title),
                style=ANTIQUE_GOLD,
            ),
            title="🌲 ✦ ELDERGROVE ✦ 🌲",
            border_style=FOREST_GREEN,
            expand=False,
        )
    )

    narration(description, loc)

    choices = event["choices"]

    puzzle_id = next(
        (
            str(choice["puzzle_id"])
            for choice in choices
            if "puzzle_id" in choice
        ),
        None,
    )

    # ----------------------------------------------
    # Puzzle Events
    # ----------------------------------------------

    if puzzle_id is not None:

        # Play mystery sound before the puzzle.
        play_sound("mystery")

        # Magical loading animation.
        show_magic_loading(loc.language)

        puzzle_solved = solve_puzzle(
            puzzle_id,
            selected_puzzles,
            journal,
            loc,
        )

        if not puzzle_solved:
            return None

        # Positive sound after solving a puzzle.
        play_sound("success")

        correct_choice = next(
            (
                choice
                for choice in choices
                if choice.get("correct")
            ),
            None,
        )

        if correct_choice is None:
            print(
                game_text(
                    loc,
                    "Error: Correct story choice not found.",
                    "خطأ: لم يتم العثور على الاختيار الصحيح.",
                )
            )
            return None

        if journal.record_solved_puzzle(puzzle_id):
            if scoring.add_points(
                "puzzles",
                puzzle_id,
                100,
            ):
                console.print(
                    Text(
                        game_text(
                            loc,
                            "🔮 +100 Puzzle Points!",
                            "🔮 +100 نقطة للألغاز!",
                        ),
                        style=ANTIQUE_GOLD,
                    )
                )

        selected_choice = correct_choice

    # ----------------------------------------------
    # Regular Story Choices
    # ----------------------------------------------

    else:
        while True:
            action_choices = []

            for index, choice in enumerate(
                choices,
                start=1,
            ):
                if loc.language == "ar":
                    choice_text = choice.get(
                        "text_ar",
                        choice["text"],
                    )
                else:
                    choice_text = choice["text"]

                action_choices.append(
                    questionary.Choice(
                        title=(
                            "✨ "
                            + loc.format_arabic(choice_text)
                        ),
                        value=index - 1,
                    )
                )

            action_choices.append(
                questionary.Choice(
                    title=(
                        "📜 "
                        + game_text(
                            loc,
                            "Review Journal",
                            "عرض دفتر الرحلة",
                        )
                    ),
                    value="journal",
                )
            )

            answer = questionary.select(
                game_text(
                    loc,
                    "Choose your action:",
                    "اختر تصرفك:",
                ),
                choices=action_choices,
                pointer="❯",
                style=MENU_STYLE,
                use_shortcuts=False,
            ).ask()

            if answer is None:
                return None

            if answer == "journal":

                # Journal opening sound.
                play_sound("journal")

                journal.display()
                continue

            selected_choice = choices[answer]
            break

        if scoring.add_points(
            "decisions",
            f"event_{event['id']}",
            40,
        ):
            console.print(
                Text(
                    game_text(
                        loc,
                        "✨ +40 Decision Points!",
                        "✨ +40 نقطة للقرارات!",
                    ),
                    style=ANTIQUE_GOLD,
                )
            )

    # ----------------------------------------------
    # Evidence Rewards
    # ----------------------------------------------

    evidence = selected_choice.get("evidence")

    if evidence and journal.add_evidence(evidence):
        if scoring.add_points(
            "evidence",
            evidence,
            25,
        ):
            console.print(
                Text(
                    game_text(
                        loc,
                        "📜 +25 Evidence Points!",
                        "📜 +25 نقطة للأدلة!",
                    ),
                    style=SOFT_GREEN,
                )
            )

    # ----------------------------------------------
    # Story Result
    # ----------------------------------------------

    if loc.language == "ar":
        result_text = selected_choice.get(
            "result_ar",
            selected_choice["result"],
        )
    else:
        result_text = selected_choice["result"]

    narration(result_text, loc)

    return selected_choice


# --------------------------------------------------
# Save Game State
# --------------------------------------------------

def build_game_state(
    explorer,
    exploration,
    journal,
    scoring,
    selected_puzzles,
    previous_choices,
    language,
):
    """Build the complete JSON-compatible save state."""

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


# --------------------------------------------------
# Main Game
# --------------------------------------------------

def run_game(saved_state=None, language="ar"):
    """Start or resume an Eldergrove adventure."""

    loc = Localization(language)

    if saved_state is not None:
        loc.set_language(
            saved_state.get("language", language)
        )

    events = localize_story(
        load_story(),
        loc.language,
    )

    events_by_id = {
        event["id"]: event
        for event in events
    }

    journal = Journal(loc)
    exploration = Exploration()
    scoring = Scoring(loc)

    # ----------------------------------------------
    # New Adventure
    # ----------------------------------------------

    if saved_state is None:

        selected_puzzles = select_random_puzzles()
        previous_choices = {}

        console.print(
            Panel(
                Text(
                    loc.display_text("game_title"),
                    style=ANTIQUE_GOLD,
                ),
                title="🌲 ✦ ELDERGROVE ✦ 🌲",
                border_style=FOREST_GREEN,
                expand=False,
            )
        )

        console.print(
            Text(
                loc.display_text("tagline"),
                style=SOFT_GREEN,
            )
        )

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
                    "لا يمكن ترك اسم المستكشف فارغًا.",
                )
            )

        explorer = Explorer(name)

        console.print(
            Text(
                loc.display_text(
                    "welcome",
                    name=explorer.name,
                ),
                style=SOFT_GREEN,
            )
        )

    # ----------------------------------------------
    # Load Saved Adventure
    # ----------------------------------------------

    else:

        explorer_data = saved_state["explorer"]
        exploration_data = saved_state["exploration"]
        journal_data = saved_state["journal"]
        scoring_data = saved_state["scoring"]

        explorer = Explorer(
            explorer_data["name"]
        )

        explorer.started_at = (
            explorer_data["started_at"]
        )

        explorer.playtime_seconds = float(
            explorer_data["playtime_seconds"]
        )

        exploration.current_region = (
            exploration_data["current_region"]
        )

        exploration.visited_locations = set(
            exploration_data["visited_locations"]
        )

        exploration.completed_locations = set(
            exploration_data["completed_locations"]
        )

        journal.evidence = list(
            journal_data["evidence"]
        )

        journal.solved_puzzles = [
            str(puzzle_id)
            for puzzle_id in journal_data["solved_puzzles"]
        ]

        journal.discoveries = list(
            journal_data["discoveries"]
        )

        scoring.scores = dict(
            scoring_data["scores"]
        )

        scoring.rewarded_actions = set(
            scoring_data["rewarded_actions"]
        )

        selected_puzzles = (
            saved_state["selected_puzzles"]
        )

        previous_choices = {
            int(event_id): choice_number
            for event_id, choice_number
            in saved_state["previous_choices"].items()
        }

        welcome = game_text(
            loc,
            "Welcome back",
            "مرحبًا بعودتك",
        )

        started = game_text(
            loc,
            "Journey started",
            "بدأت الرحلة",
        )

        console.print(
            Text(
                f"{welcome}: "
                f"{loc.format_arabic(explorer.name)}!",
                style=SOFT_GREEN,
            )
        )

        console.print(
            f"{started}: {explorer.started_at}"
        )

    # ----------------------------------------------
    # Enter the Forest
    # ----------------------------------------------

    input(
        game_text(
            loc,
            "\nPress Enter to enter the forest...",
            "\nاضغط Enter لدخول الغابة...",
        )
    )

    # Play the forest entry animation.
    show_forest_entry(loc.language)

    game_finished = False

    explorer.start_session()

    try:

        # Start the looping forest ambience.
        play_forest()

        # ------------------------------------------
        # Exploration Loop
        # ------------------------------------------

        while not game_finished:

            exploration.show_locations(loc)

            answer = choose_exploration_action(
                exploration,
                loc,
            )

            if answer is None:
                break

            # --------------------------------------
            # Journal
            # --------------------------------------

            if answer == "j":

                play_sound("journal")

                journal.display()
                continue

            # --------------------------------------
            # Score
            # --------------------------------------

            if answer == "s":

                play_sound("success")

                scoring.display_score()
                continue

            # --------------------------------------
            # Playtime
            # --------------------------------------

            if answer == "t":

                play_sound("success")

                label = game_text(
                    loc,
                    "Playtime",
                    "مدة اللعب",
                )

                console.print(
                    f"\n{label}: "
                    f"{explorer.get_duration_text()}"
                )
                continue

            # --------------------------------------
            # Save
            # --------------------------------------

            if answer == "v":

                state = build_game_state(
                    explorer,
                    exploration,
                    journal,
                    scoring,
                    selected_puzzles,
                    previous_choices,
                    loc.language,
                )

                save_game(state)
                continue

            

            if answer == "q":

                console.print(
                    game_text(
                        loc,
                        "Leaving the forest...",
                        "تغادر الغابة...",
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
                        "خيار غير صحيح، حاول مجددًا.",
                    )
                )
                continue

            location = exploration.visit_location(
                int(answer),
                loc,
            )

            if location is None:
                continue

            location_id = location["id"]

            

            if (
                location_id
                in exploration.completed_locations
            ):

                print(
                    game_text(
                        loc,
                        "You have already explored this location.",
                        "لقد استكشفت هذا الموقع مسبقًا.",
                    )
                )

                input(
                    game_text(
                        loc,
                        "\nPress Enter to return...",
                        "\nاضغط Enter للعودة...",
                    )
                )
                continue

            

            event_id = location.get("event_id")

            if event_id == 1:

                # Play the ancient stone gate sound.
                play_sound("gate")

           

            if event_id is not None:

                event = events_by_id.get(event_id)

                if event is None:

                    print(
                        game_text(
                            loc,
                            "Error: Story event not found.",
                            "خطأ: لم يتم العثور على حدث القصة.",
                        )
                    )
                    continue

                show_forest_memory(
                    event_id,
                    previous_choices,
                    journal,
                    loc,
                )

                result = play_event(
                    event,
                    journal,
                    selected_puzzles,
                    scoring,
                    loc,
                )

                if result is None:

                    print(
                        game_text(
                            loc,
                            "This event could not be completed.",
                            "تعذر إكمال هذا الحدث.",
                        )
                    )
                    continue

                if event_id not in (3, 5, 7, 8):

                    choice_number = (
                        event["choices"].index(result)
                        + 1
                    )

                    previous_choices[event_id] = (
                        choice_number
                    )

            # --------------------------------------
            # Secret Location
            # --------------------------------------

            else:

                narration(
                    (
                        "تستكشف المكان وتكشف أسراره."
                        if loc.language == "ar"
                        else (
                            "You explore the area "
                            "and uncover its secrets."
                        )
                    ),
                    loc,
                )

            # --------------------------------------
            # Secret Reward
            # --------------------------------------

            if location.get("optional", False):

                if scoring.add_points(
                    "secrets",
                    location_id,
                    50,
                ):

                    show_secret_discovery(
                        loc.language,
                        points=50,
                    )

            # --------------------------------------
            # Complete Location
            # --------------------------------------

            exploration.complete_location(
                location_id
            )

            console.print(
                Text(
                    game_text(
                        loc,
                        "✨ Location completed!",
                        "✨ اكتمل استكشاف الموقع!",
                    ),
                    style=SOFT_GREEN,
                )
            )

            # --------------------------------------
            # Final Passage
            # --------------------------------------

            if location_id == "last_passage":

                game_finished = True
                break

            input(
                game_text(
                    loc,
                    "\nPress Enter to continue...",
                    "\nاضغط Enter للمتابعة...",
                )
            )

    finally:

        # Always stop the timer and audio when
        # leaving the exploration loop.
        explorer.pause_session()

        stop_all_audio()

    # --------------------------------------------------
    # Ending
    # --------------------------------------------------

    if game_finished:

        # Final magical animation.
        show_final_fate(loc.language)

        fate_id = determine_fate(scoring)

        save_explorer_record(
            explorer,
            scoring.get_total(),
            fate_id,
            loc,
        )

        display_ending(fate_id, loc)

        # ----------------------------------------------
        # Journey Summary
        # ----------------------------------------------

        console.print(
            Panel(
                Text(
                    game_text(
                        loc,
                        "JOURNEY SUMMARY",
                        "ملخص الرحلة",
                    ),
                    style=ANTIQUE_GOLD,
                ),
                border_style=FOREST_GREEN,
                expand=False,
            )
        )

        explorer_label = game_text(
            loc,
            "Explorer",
            "المستكشف",
        )

        started_label = game_text(
            loc,
            "Journey started",
            "بدأت الرحلة",
        )

        playtime_label = game_text(
            loc,
            "Playtime",
            "مدة اللعب",
        )

        console.print(
            f"{explorer_label}: "
            f"{loc.format_arabic(explorer.name)}"
        )

        console.print(
            f"{started_label}: "
            f"{explorer.started_at}"
        )

        console.print(
            f"{playtime_label}: "
            f"{explorer.get_duration_text()}"
        )

        scoring.display_score()
        journal.display()

        console.print(
            Text(
                game_text(
                    loc,
                    "🌲 The forest will remember your name.",
                    "🌲 ستتذكر الغابة اسمك.",
                ),
                style=ANTIQUE_GOLD,
            )
        )