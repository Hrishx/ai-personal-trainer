class RepPhaseEngine:

    def __init__(self):
        self.previous_angle = None
        self.phase = "LOCKOUT"

    def update(self, knee_angle):

        if self.previous_angle is None:
            self.previous_angle = knee_angle
            return self.phase

        delta = knee_angle - self.previous_angle

        # descending
        if delta < -1:
            self.phase = "ECCENTRIC"

        # bottom position
        elif knee_angle < 95:
            self.phase = "BOTTOM"

        # ascending
        elif delta > 1 and knee_angle < 170:
            self.phase = "CONCENTRIC"

        # standing
        elif knee_angle >= 170:
            self.phase = "LOCKOUT"

        self.previous_angle = knee_angle

        return self.phase