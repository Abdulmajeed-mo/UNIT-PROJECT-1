# التنقل بين المواقع وشروط فتحها

import json
from pathlib import Path

LOCATIONS_FILE = Path(__file__).parent / "data" / "locations.json"
LOCATIONS_AR_FILE = Path(__file__).parent / "data" / "locations_ar.json"


def load_locations():
    with LOCATIONS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data["regions"]


class Exploration:
    def __init__(self):
        self.regions = load_locations()

        with LOCATIONS_AR_FILE.open("r", encoding="utf-8") as file:
            arabic_regions = json.load(file)["regions"]

        self.arabic_texts = {}

        for region in arabic_regions:
            original_region = next(
                item for item in self.regions
                if item["id"] == region["id"]
            )

            self.arabic_texts[original_region["name"]] = region["name"]
            self.arabic_texts[original_region["description"]] = region["description"]

            for location in region["locations"]:
                original_location = next(
                    item for item in original_region["locations"]
                    if item["id"] == location["id"]
                )

                self.arabic_texts[original_location["name"]] = location["name"]
                self.arabic_texts[original_location["description"]] = location["description"]

        self.current_region = 0
        self.visited_locations = set()
        self.completed_locations = set()

    def get_current_region(self):
        return self.regions[self.current_region]

    def get_locations(self):
        return self.get_current_region()["locations"]

    def is_unlocked(self, location):
        requirements = location.get("requires", [])

        return all(
            required in self.completed_locations
            for required in requirements
        )

    def translate_location(self, text, loc):
        if loc.language == "ar":
            text = self.arabic_texts.get(text, text)

        return loc.format_arabic(text)

    def show_locations(self, loc):
        region = self.get_current_region()

        print("\n" + "=" * 45)
        print(self.translate_location(region["name"], loc))
        print("=" * 45)

        print(self.translate_location(region["description"], loc))
        print(f"\n{loc.display_text('available_locations')}:")

        for index, location in enumerate(self.get_locations(), start=1):
            if location["id"] in self.completed_locations:
                status = loc.display_text("completed")
            elif self.is_unlocked(location):
                status = loc.display_text("available")
            else:
                status = loc.display_text("locked")

            name = self.translate_location(location["name"], loc)
            print(f"{index}. {name} [{status}]")

    def visit_location(self, location_number, loc):
        locations = self.get_locations()

        if not 1 <= location_number <= len(locations):
            print(loc.display_text("invalid_option"))
            return None

        location = locations[location_number - 1]

        if not self.is_unlocked(location):
            message = (
                "هذا الموقع لا يزال مغلقًا."
                if loc.language == "ar"
                else "This location is locked."
            )
            print(loc.format_arabic(message))
            return None

        self.visited_locations.add(location["id"])

        name = self.translate_location(location["name"], loc)
        print(f"\n--- {name} ---")
        print(self.translate_location(location["description"], loc))

        return location

    def move_to_next_region(self, loc):
        region = self.get_current_region()

        required_locations = [
            location["id"]
            for location in region["locations"]
            if not location.get("optional", False)
        ]

        if not all(
            location_id in self.completed_locations
            for location_id in required_locations
        ):
            message = (
                "أكمل المواقع الرئيسية قبل مغادرة المنطقة."
                if loc.language == "ar"
                else "Complete all main locations before leaving this region."
            )
            print(loc.format_arabic(message))
            return False

        if self.current_region + 1 >= len(self.regions):
            message = (
                "لقد وصلت إلى المنطقة الأخيرة."
                if loc.language == "ar"
                else "You have reached the final region."
            )
            print(loc.format_arabic(message))
            return False

        self.current_region += 1

        name = self.translate_location(
            self.get_current_region()["name"], loc
        )
        print(f"\n{name}")

        return True

    def complete_location(self, location_id):
        self.visited_locations.add(location_id)
        self.completed_locations.add(location_id)