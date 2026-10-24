# يعرض القوائم والنصوص بشكل جميل


# Displays the main menu with Arabic and English support.

from game.engine import run_game
from game.save_system import load_game
from game.explorers import display_hall
from game.localization import Localization


def show_main_menu():
    loc = Localization()  # Arabic is the default language.

    while True:
        print("\n" + "=" * 45)
        print(loc.display_text("game_title"))
        print("=" * 45)
        print(loc.display_text("tagline"))

        print(f"1. {loc.display_text('start_game')}")
        print(f"2. {loc.display_text('continue_game')}")
        print(f"3. {loc.display_text('hall_of_explorers')}")
        language_option = ("English"
            if loc.language == "ar"
            else loc.format_arabic("العربية"))

        print(f"4. {language_option}")
        print(f"5. {loc.display_text('exit')}")

        choice = input(
            f"\n{loc.display_text('select_option')} "
        ).strip()

        if choice == "1":
            run_game(language=loc.language)

        elif choice == "2":
            saved_state = load_game()

            if saved_state is not None:
                saved_language = saved_state.get("language", loc.language)
                run_game(saved_state, language=saved_language)

        elif choice == "3":
            display_hall(loc)

        elif choice == "4":
            new_language = "en" if loc.language == "ar" else "ar"
            loc.set_language(new_language)

        elif choice == "5":
            print("\nThank you for playing Eldergrove.")
            break

        else:
            print("Invalid option. Please try again.")
