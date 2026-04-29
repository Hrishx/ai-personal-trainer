import numpy as np
import time


class BiomechanicsEngine:

    def __init__(self):

        self.rep_count = 0
        self.state = "UP"
        self.prev_state = "UP"

        # NEW: rep protection
        self.rep_cooldown = 0
        self.cooldown_frames = 3

        # NEW: rep debounce time
        self.last_rep_time = 0
        self.min_rep_time = 0.2

    # ----------------------
    # ANGLE CALCULATION
    # ----------------------

    def calculate_angle(self, a, b, c):

        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        ba = a - b
        bc = c - b

        cosine = np.dot(ba, bc) / (
            np.linalg.norm(ba) * np.linalg.norm(bc)
        )

        cosine = np.clip(cosine, -1, 1)

        return np.degrees(np.arccos(cosine))

    # ----------------------
    # REP SAFE COUNT
    # ----------------------

    def register_rep(self):

        current_time = time.time()

        if (
            self.rep_cooldown == 0 and
            current_time - self.last_rep_time > self.min_rep_time
        ):
            self.rep_count += 1
            self.rep_cooldown = self.cooldown_frames
            self.last_rep_time = current_time

    # ----------------------
    # SQUAT
    # ----------------------

    def analyze_squat(self, landmarks, frame_shape):

        h, w, _ = frame_shape

        hip = landmarks[24]
        knee = landmarks[26]
        ankle = landmarks[28]
        shoulder = landmarks[12]

        hip_p = (hip.x * w, hip.y * h)
        knee_p = (knee.x * w, knee.y * h)
        ankle_p = (ankle.x * w, ankle.y * h)
        shoulder_p = (shoulder.x * w, shoulder.y * h)

        knee_angle = self.calculate_angle(hip_p, knee_p, ankle_p)
        back_angle = self.calculate_angle(shoulder_p, hip_p, knee_p)

        knee_offset = landmarks[25].x - landmarks[27].x
        hip_depth = knee.y - hip.y

        # -------- STATE MACHINE --------

        if knee_angle < 110:
            self.state = "DOWN"

        elif knee_angle > 160:

            self.state = "UP"

            if self.prev_state == "DOWN":
                self.register_rep()

        self.prev_state = self.state

        # cooldown countdown
        if self.rep_cooldown > 0:
            self.rep_cooldown -= 1

        return {
            "knee_angle": knee_angle,
            "back_angle": back_angle,
            "knee_offset": knee_offset,
            "hip_depth": hip_depth,
            "rep_count": self.rep_count,
            "state": self.state
        }

    # ----------------------
    # PUSHUP
    # ----------------------

    def analyze_pushup(self, landmarks, frame_shape):

        h, w, _ = frame_shape

        shoulder = landmarks[12]
        elbow = landmarks[14]
        wrist = landmarks[16]

        shoulder_p = (shoulder.x * w, shoulder.y * h)
        elbow_p = (elbow.x * w, elbow.y * h)
        wrist_p = (wrist.x * w, wrist.y * h)

        elbow_angle = self.calculate_angle(
            shoulder_p,
            elbow_p,
            wrist_p
        )

        if elbow_angle < 90:
            self.state = "DOWN"

        elif elbow_angle > 160:

            self.state = "UP"

            if self.prev_state == "DOWN":
                self.register_rep()

        self.prev_state = self.state

        if self.rep_cooldown > 0:
            self.rep_cooldown -= 1

        return {
            "knee_angle": 90,
            "back_angle": 90,
            "knee_offset": 0,
            "hip_depth": 0,
            "rep_count": self.rep_count,
            "state": self.state
        }

    # ----------------------
    # LUNGE
    # ----------------------

    def analyze_lunge(self, landmarks, frame_shape):

        h, w, _ = frame_shape

        hip = landmarks[24]
        knee = landmarks[26]
        ankle = landmarks[28]

        hip_p = (hip.x * w, hip.y * h)
        knee_p = (knee.x * w, knee.y * h)
        ankle_p = (ankle.x * w, ankle.y * h)

        knee_angle = self.calculate_angle(
            hip_p,
            knee_p,
            ankle_p
        )

        if knee_angle < 100:
            self.state = "DOWN"

        elif knee_angle > 160:

            self.state = "UP"

            if self.prev_state == "DOWN":
                self.register_rep()

        self.prev_state = self.state

        if self.rep_cooldown > 0:
            self.rep_cooldown -= 1

        return {
            "knee_angle": knee_angle,
            "back_angle": 90,
            "knee_offset": 0,
            "hip_depth": 0,
            "rep_count": self.rep_count,
            "state": self.state
        }

    # ----------------------
    # PLANK
    # ----------------------

    def analyze_plank(self, landmarks, frame_shape):

        return {
            "knee_angle": 90,
            "back_angle": 90,
            "knee_offset": 0,
            "hip_depth": 0,
            "rep_count": 0,
            "state": "HOLD"
        }