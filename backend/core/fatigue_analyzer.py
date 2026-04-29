class FatigueAnalyzer:

    def __init__(self):
        self.history = []
        self.started = False

    def analyze(self, posture_state):

        # -----------------------------
        # Detect workout start
        # -----------------------------
        rep = posture_state.get("rep_count", 0)
        phase = posture_state.get("rep_phase", "LOCKOUT")

        if rep > 0 or phase != "LOCKOUT":
            self.started = True

        # If workout not started yet
        if not self.started:
            posture_state["fatigue_level"] = "fresh"
            return posture_state

        # -----------------------------
        # Store posture history
        # -----------------------------
        self.history.append(posture_state)

        if len(self.history) > 10:
            self.history.pop(0)

        fatigue = "fresh"

        # -----------------------------
        # Analyze recent frames
        # -----------------------------
        recent = self.history[-5:]

        bad = 0

        for state in recent:

            severity = state.get("severity_score", 0)

            if severity >= 2:
                bad += 1

        # -----------------------------
        # Fatigue detection rule
        # -----------------------------
        if bad >= 3:
            fatigue = "fatigued"

        posture_state["fatigue_level"] = fatigue

        return posture_state