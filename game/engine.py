# يدير تقدم اللاعب بين الأحداث


from game.story import load_story


def run_game():
    events = load_story()

    print("\n" + "=" * 45)
    print("       ELDERGROVE: THE FORGOTTEN FOREST")
    print("=" * 45)
    print("The forest remembers. Will you escape?")

    input("\nPress Enter to begin...")

    for event in events:
        print("\n" + "=" * 45)
        print(f"\n{event['title']}\n")
        print(event["description"])

        print("\nChoose your action:")

        for index, choice in enumerate(event["choices"], start=1):
            print(f"{index}. {choice['text']}")

        while True:
            answer = input("\nYour choice: ").strip()

            if answer.isdigit():
                choice_number = int(answer)

                if 1 <= choice_number <= len(event["choices"]):
                    selected_choice = event["choices"][choice_number - 1]
                    break

            print("Invalid choice. Please try again.")

        print(f"\n{selected_choice['result']}")
        input("\nPress Enter to continue...")

    print("\n" + "=" * 45)
    print("You have reached the end of the current story.")
    print("=" * 45)
