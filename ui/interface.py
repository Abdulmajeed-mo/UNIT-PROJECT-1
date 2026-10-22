# يعرض القوائم والنصوص بشكل جميل


from game.engine import run_game
from game.save_system import load_game
from game.explorers import display_hall

def show_main_menu():
    while True:
        print("\n" + "=" * 45)
        print("       ELDERGROVE: THE FORGOTTEN FOREST")
        print("=" * 45)
        print("1. Start New Game")
        print("2. Continue Game")
        print("3. Hall of Lost Explorers")
        print("4. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            run_game()

        elif choice == "2":
            saved_state = load_game()

            if saved_state is not None:
                run_game(saved_state)

        elif choice == "3":
            display_hall()

        elif choice == "4":
            print("\nThank you for playing Eldergrove.")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")
