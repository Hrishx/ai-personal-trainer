class InjuryRiskEngine:

    def __init__(self):
        self.history = []

    def update(self, errors):

        self.history.append(errors)

        if len(self.history) > 10:
            self.history.pop(0)

    def assess_risk(self):

        knee_count = 0
        back_count = 0

        for frame_errors in self.history:

            if "knee_valgus" in frame_errors:
                knee_count += 1

            if "forward_lean" in frame_errors:
                back_count += 1

        risks = []

        if knee_count > 4:
            risks.append("ACL strain risk due to knee collapse")

        if back_count > 4:
            risks.append("Lumbar stress risk due to forward lean")

        return risks