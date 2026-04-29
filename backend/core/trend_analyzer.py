class TrendAnalyzer:

    def __init__(self):
        self.previous_state = None
        self.previous_knee = None
        self.previous_back = None
        self.previous_depth = None

    def analyze(self, posture_state):

        knee_status = posture_state["knee_status"]
        back_status = posture_state["back_status"]
        depth_status = posture_state["depth_status"]

        trend = {
            "knee_trend": "stable",
            "back_trend": "stable",
            "depth_trend": "stable"
        }

        # Knee trend
        if self.previous_knee:
            if knee_status != self.previous_knee:
                trend["knee_trend"] = "changing"

        # Back trend
        if self.previous_back:
            if back_status != self.previous_back:
                trend["back_trend"] = "changing"

        # Depth trend
        if self.previous_depth:
            if depth_status != self.previous_depth:
                trend["depth_trend"] = "changing"

        self.previous_knee = knee_status
        self.previous_back = back_status
        self.previous_depth = depth_status

        posture_state.update(trend)

        return posture_state