# يسجل الأدلة التي اكتشفها اللاعب


# Tracks evidence, solved puzzles, and discoveries.


class Journal:
    CONNECTIONS = {
        "forest_memory": {
            "requires": [
                "The forest remembers every visitor.",
                "The forest uses voices to mislead travelers."
            ],
            "title": "The Forest Remembers",
            "description": "The forest remembers explorers and uses their memories to guide or mislead them."
        },
        "hidden_trials": {
            "requires": [
                "The forgotten chronicle contains the forest's truth.",
                "The forest conceals its purpose behind trials."
            ],
            "title": "The Hidden Trials",
            "description": "The forest's challenges are deliberate tests, not random obstacles."
        },
        "ancient_symbols": {
            "requires": [
                "The moon comes before the sun.",
                "The correct symbol order is Moon, Sun, Root."
            ],
            "title": "The Ancient Order",
            "description": "The symbols reveal a meaningful sequence that unlocks the forest's secrets."
        }
    }

    def __init__(self):
        self.evidence = []
        self.solved_puzzles = []
        self.discoveries = []

    def add_evidence(self, evidence):
        if not evidence or evidence in self.evidence:
            return False

        self.evidence.append(evidence)
        print(f"\nEvidence added to your journal: {evidence}")
        self.check_connections()
        return True

    def record_solved_puzzle(self, puzzle_id):
        puzzle_id = str(puzzle_id)

        if puzzle_id in self.solved_puzzles:
            return False

        self.solved_puzzles.append(puzzle_id)
        return True

    def check_connections(self):
        for connection_id, connection in self.CONNECTIONS.items():
            if connection_id in self.discoveries:
                continue

            if all(
                clue in self.evidence
                for clue in connection["requires"]
            ):
                self.discoveries.append(connection_id)
                print(f"\nNEW DISCOVERY: {connection['title']}")
                print(connection["description"])

    def display(self):
        print("\n" + "=" * 45)
        print("             YOUR JOURNAL")
        print("=" * 45)

        print("\nDiscovered Evidence:")
        if self.evidence:
            for index, evidence in enumerate(self.evidence, start=1):
                print(f"{index}. {evidence}")
        else:
            print("No evidence discovered yet.")

        puzzle_names = {
            "1": "The First Riddle",
            "2": "The Rune Equation",
            "3": "The Three Forgotten Symbols",
            "4": "The Missing Chronicle",
        }

        print("\nSolved Puzzles:")
        if self.solved_puzzles:
            for puzzle_id in self.solved_puzzles:
                print(f"- {puzzle_names.get(str(puzzle_id), 'Unknown Puzzle')}")
        else:
            print("No puzzles solved yet.")

        print("\nDiscoveries:")
        if self.discoveries:
            for discovery_id in self.discoveries:
                print(f"- {self.CONNECTIONS[discovery_id]['title']}")
        else:
            print("No discoveries unlocked yet.")

        print("=" * 45)
