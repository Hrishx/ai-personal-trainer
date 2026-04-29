import numpy as np
from collections import Counter


class ExerciseDetector:

    def __init__(self):

        self.frame_buffer = []
        self.buffer_size = 30

    def detect_exercise(self, landmarks):

        if not landmarks:
            return "unknown", 0

        shoulder = np.array([landmarks[12].x, landmarks[12].y])
        hip = np.array([landmarks[24].x, landmarks[24].y])
        knee = np.array([landmarks[26].x, landmarks[26].y])
        ankle = np.array([landmarks[28].x, landmarks[28].y])
        wrist = np.array([landmarks[16].x, landmarks[16].y])

        torso_angle = self._angle(shoulder, hip, knee)
        knee_angle = self._angle(hip, knee, ankle)

        hip_height = hip[1]
        wrist_height = wrist[1]

        exercise = "unknown"

        # -------- SQUAT --------
        if knee_angle < 170 and torso_angle > 10:
            exercise = "squat"

        # -------- PUSHUP --------
        elif wrist_height > hip_height and abs(torso_angle - 90) < 25:
            exercise = "pushup"

        # -------- LUNGE --------
        elif 60 < knee_angle < 120 and torso_angle > 60:
            exercise = "lunge"

        # -------- PLANK --------
        elif abs(torso_angle - 90) < 15:
            exercise = "plank"

        # -------- BUFFER --------

        self.frame_buffer.append(exercise)

        if len(self.frame_buffer) > self.buffer_size:
            self.frame_buffer.pop(0)

        # wait until buffer fills
        if len(self.frame_buffer) < 10:
            return exercise, 0.5

        most_common = Counter(self.frame_buffer).most_common(1)[0]

        confidence = most_common[1] / len(self.frame_buffer)

        return most_common[0], confidence

    def _angle(self, a, b, c):

        ba = a - b
        bc = c - b

        cosine = np.dot(ba, bc) / (
            np.linalg.norm(ba) * np.linalg.norm(bc)
        )

        cosine = np.clip(cosine, -1, 1)

        return np.degrees(np.arccos(cosine))