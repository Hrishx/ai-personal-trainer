class RealtimeCoach:

    def __init__(self):
        self.cooldown = 0
        self.last_feedback = None

    def get_feedback(self, posture_state, errors, phase):

        if self.cooldown > 0:
            self.cooldown -= 1
            return None

        # error priority
        if "knee_valgus" in errors:
            self.cooldown = 40
            return "Push your knees outward"

        if "forward_lean" in errors:
            self.cooldown = 40
            return "Keep your chest up"

        if "shallow_depth" in errors:
            self.cooldown = 40
            return "Go deeper into the squat"

        # phase coaching
        if phase == "ECCENTRIC":
            self.cooldown = 30
            return "Control the descent"

        if phase == "CONCENTRIC":
            self.cooldown = 30
            return "Drive up"

        if phase == "LOCKOUT":
            self.cooldown = 30
            return "Stand tall"

        return None