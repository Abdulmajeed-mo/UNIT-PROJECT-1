# يعرض القوائم والنصوص بشكل جميل


from game.engine import run_game


def show_main_menu():
    while True:
        print("\n" + "=" * 45)
        print("       ELDERGROVE: THE FORGOTTEN FOREST")
        print("=" * 45)
        print("1. Start New Game")
        print("2. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            run_game()
        elif choice == "2":
            print("\nThank you for playing Eldergrove.")
            break
        else:
            print("Invalid choice. Please select 1 or 2.")
