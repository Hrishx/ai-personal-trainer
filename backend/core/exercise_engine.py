import json


class ExerciseEngine:
    def __init__(self, json_path="data/exercise_data.json"):
        with open(json_path, "r") as f:
            self.exercise_data = json.load(f)

    def get_exercise_rules(self, exercise_name):
        return self.exercise_data.get(exercise_name, None)
