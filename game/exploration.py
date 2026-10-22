# التنقل بين المواقع وشروط فتحها

import json
from pathlib import Path


LOCATIONS_FILE = Path(__file__).parent / "data" / "locations.json"


def load_locations():
    with LOCATIONS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data["regions"]


class Exploration:
    def __init__(self):
        self.regions = load_locations()
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

    def show_locations(self):
        region = self.get_current_region()

        print("\n" + "=" * 45)
        print(f"       {region['name']}")
        print("=" * 45)
        print(region["description"])

        print("\nAvailable Locations:")

        for index, location in enumerate(
            self.get_locations(), start=1
        ):
            if location["id"] in self.completed_locations:
                status = "Completed"
            elif self.is_unlocked(location):
                status = "Available"
            else:
                status = "Locked"

            print(f"{index}. {location['name']} [{status}]")

        print("B. Back")

    def visit_location(self, location_number):
        locations = self.get_locations()

        if not 1 <= location_number <= len(locations):
            print("Invalid location.")
            return None

        location = locations[location_number - 1]

        if not self.is_unlocked(location):
            print("This location is locked.")
            return None

        self.visited_locations.add(location["id"])

        print(f"\n--- {location['name']} ---")
        print(location["description"])

        return location

    def complete_location(self, location_id):
        self.visited_locations.add(location_id)
        self.completed_locations.add(location_id)

    

    def move_to_next_region(self):
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
            print("\nComplete all main locations before leaving this region.")
            return False

        if self.current_region + 1 >= len(self.regions):
            print("\nYou have reached the final region.")
            return False

        self.current_region += 1

        print(f"\nEntering {self.get_current_region()['name']}...")
        return True


