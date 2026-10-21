# يسجل الأدلة التي اكتشفها اللاعب


class Journal:
    def __init__(self):
        self.evidence = []
        self.solved_puzzles = []

    def add_evidence(self, evidence):
        if evidence and evidence not in self.evidence:
            self.evidence.append(evidence)
            print(f"\nEvidence added to your journal: {evidence}")

    def record_solved_puzzle(self, puzzle_id):
        if puzzle_id not in self.solved_puzzles:
            self.solved_puzzles.append(puzzle_id)

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

        print("\nSolved Puzzles:")
        if self.solved_puzzles:
            for puzzle_id in self.solved_puzzles:
                print(f"- {puzzle_id.replace('_', ' ').title()}")
        else:
            print("No puzzles solved yet.")

        print("=" * 45)
