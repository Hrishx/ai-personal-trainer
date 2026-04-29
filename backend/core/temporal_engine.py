import time
import numpy as np


class TemporalEngine:

    def __init__(self, window_size=30):
        self.window_size = window_size
        self.knee_history = []
        self.timestamps = []

    def update(self, knee_angle):

        now = time.time()

        self.knee_history.append(knee_angle)
        self.timestamps.append(now)

        if len(self.knee_history) > self.window_size:
            self.knee_history.pop(0)
            self.timestamps.pop(0)

    def get_velocity(self):

        if len(self.knee_history) < 2:
            return 0

        angle_diff = self.knee_history[-1] - self.knee_history[-2]
        time_diff = self.timestamps[-1] - self.timestamps[-2]

        if time_diff == 0:
            return 0

        return angle_diff / time_diff

    def get_smoothness(self):

        if len(self.knee_history) < 5:
            return 1.0

        diffs = np.diff(self.knee_history)
        variance = np.var(diffs)

        smoothness = max(0, 1 - variance / 50)

        return smoothness
    
    def reset(self):
        self.prev_angle = None
        self.speeds = []