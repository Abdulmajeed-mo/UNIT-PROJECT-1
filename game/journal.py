# يسجل الأدلة التي اكتشفها اللاعب


# Tracks evidence, solved puzzles, and discoveries.
# Journal data and translations are stored in JSON files.

import json
from pathlib import Path

from game.localization import Localization


DATA_DIR = Path(__file__).parent / "data"
JOURNAL_FILE = DATA_DIR / "journal.json"
JOURNAL_AR_FILE = DATA_DIR / "journal_ar.json"


def load_journal_data(file_path):
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


class Journal:
    def __init__(self, loc=None):
        self.loc = loc if loc is not None else Localization("en")

        self.data = load_journal_data(JOURNAL_FILE)
        self.arabic_data = load_journal_data(JOURNAL_AR_FILE)

        self.connections = self.data["connections"]

        self.evidence = []
        self.solved_puzzles = []
        self.discoveries = []

    def show_text(self, english, arabic):
        text = arabic if self.loc.language == "ar" else english
        return self.loc.format_arabic(text)

    def translate_evidence(self, evidence):
        if self.loc.language == "ar":
            text = self.arabic_data["evidence"].get(
                evidence, evidence
            )
        else:
            text = evidence

        return self.loc.format_arabic(text)

    def discovery_text(self, discovery_id, field):
        if self.loc.language == "ar":
            translation = self.arabic_data["connections"].get(
                discovery_id, {}
            )

            text = translation.get(
                field,
                self.connections[discovery_id][field]
            )
        else:
            text = self.connections[discovery_id][field]

        return self.loc.format_arabic(text)

    def add_evidence(self, evidence):
        if not evidence or evidence in self.evidence:
            return False

        # Keep original evidence for discovering connections.
        self.evidence.append(evidence)

        label = self.show_text(
            "Evidence added to your journal:",
            "تمت إضافة دليل إلى دفتر الرحلة:"
        )

        print(f"\n{label} {self.translate_evidence(evidence)}")

        self.check_connections()
        return True

    def record_solved_puzzle(self, puzzle_id):
        puzzle_id = str(puzzle_id)

        if puzzle_id in self.solved_puzzles:
            return False

        self.solved_puzzles.append(puzzle_id)
        return True

    def check_connections(self):
        for connection_id, connection in self.connections.items():
            if connection_id in self.discoveries:
                continue

            if all(
                clue in self.evidence
                for clue in connection["requires"]
            ):
                self.discoveries.append(connection_id)

                label = self.show_text(
                    "NEW DISCOVERY:",
                    "اكتشاف جديد:"
                )

                title = self.discovery_text(connection_id, "title")
                description = self.discovery_text(
                    connection_id, "description"
                )

                print(f"\n{label} {title}")
                print(description)

    def display(self):
        print("\n" + "=" * 45)
        print(self.show_text("YOUR JOURNAL", "دفتر رحلتك"))
        print("=" * 45)

        print(
            "\n" + self.show_text(
                "Discovered Evidence:",
                "الأدلة المكتشفة:"
            )
        )

        if self.evidence:
            for index, evidence in enumerate(self.evidence, start=1):
                print(
                    f"{index}. {self.translate_evidence(evidence)}"
                )
        else:
            print(
                self.show_text(
                    "No evidence discovered yet.",
                    "لم تكتشف أي أدلة بعد."
                )
            )

        print(
            "\n" + self.show_text(
                "Solved Puzzles:",
                "الألغاز المحلولة:"
            )
        )

        puzzle_names = self.data["puzzle_names"]

        if self.loc.language == "ar":
            puzzle_names = self.arabic_data["puzzle_names"]

        if self.solved_puzzles:
            for puzzle_id in self.solved_puzzles:
                name = puzzle_names.get(
                    str(puzzle_id), "Unknown Puzzle"
                )
                print(f"- {self.loc.format_arabic(name)}")
        else:
            print(
                self.show_text(
                    "No puzzles solved yet.",
                    "لم تحل أي ألغاز بعد."
                )
            )

        print(
            "\n" + self.show_text(
                "Discoveries:",
                "الاكتشافات:"
            )
        )

        if self.discoveries:
            for discovery_id in self.discoveries:
                if discovery_id in self.connections:
                    title = self.discovery_text(
                        discovery_id, "title"
                    )
                    print(f"- {title}")
        else:
            print(
                self.show_text(
                    "No discoveries unlocked yet.",
                    "لم تفتح أي اكتشافات بعد."
                )
            )

        print("=" * 45)
