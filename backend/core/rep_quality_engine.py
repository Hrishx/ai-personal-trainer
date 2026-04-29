class RepQualityEngine:

    def score_rep(self, posture_state, biomech_data, smoothness):

        score = 100

        knee_angle = biomech_data["knee_angle"]
        back_angle = biomech_data["back_angle"]

        depth_error = abs(95 - knee_angle)
        score -= min(depth_error * 0.3, 15)

        back_error = abs(80 - back_angle)
        score -= min(back_error * 0.2, 15)

        if posture_state["knee_status"] == "mild_valgus":
            score -= 10

        if posture_state["knee_status"] == "moderate_valgus":
            score -= 20

        smooth_penalty = (1 - smoothness) * 10
        score -= smooth_penalty

        score = max(min(score, 100), 0)

        return int(score)
