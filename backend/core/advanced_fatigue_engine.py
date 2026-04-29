class AdvancedFatigueEngine:

    def __init__(self):
        self.rep_scores = []

    def update(self, score):

        self.rep_scores.append(score)

        if len(self.rep_scores) > 10:
            self.rep_scores.pop(0)

    def detect_fatigue(self):

        if len(self.rep_scores) < 4:
            return "fresh"

        recent = self.rep_scores[-3:]

        if recent[0] > recent[1] > recent[2]:
            return "fatigue_increasing"

        if sum(recent) / len(recent) < 60:
            return "fatigued"

        return "fresh"
    def reset(self):
        self.rep_scores = []