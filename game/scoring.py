# Manages explorer scores and prevents duplicate rewards.


class Scoring:
    MAX_SCORES = {
        "puzzles": 400,
        "evidence": 250,
        "decisions": 200,
        "secrets": 150,
    }

    def __init__(self):
        self.scores = {
            category: 0
            for category in self.MAX_SCORES
        }
        self.rewarded_actions = set()

    def add_points(self, category, action_id, points):
        if category not in self.scores:
            return False

        reward_key = f"{category}:{action_id}"

        if reward_key in self.rewarded_actions:
            return False

        if points <= 0:
            return False

        maximum = self.MAX_SCORES[category]
        remaining = maximum - self.scores[category]

        if remaining <= 0:
            return False

        awarded = min(points, remaining)

        self.scores[category] += awarded
        self.rewarded_actions.add(reward_key)

        return True

    def get_total(self):
        return sum(self.scores.values())

    def display_score(self):
        print("\n" + "=" * 45)
        print("             EXPLORER SCORE")
        print("=" * 45)

        for category, score in self.scores.items():
            maximum = self.MAX_SCORES[category]
            print(f"{category.title()}: {score}/{maximum}")

        print("-" * 45)
        print(f"TOTAL: {self.get_total()}/1000")
