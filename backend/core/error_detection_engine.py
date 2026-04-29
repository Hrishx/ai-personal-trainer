class ErrorDetectionEngine:

    def detect(self, posture_state, biomech_data):

        errors = []

        knee = posture_state["knee_status"]
        back = posture_state["back_status"]
        depth = posture_state["depth_status"]

        if knee == "moderate_valgus":
            errors.append("knee_valgus")

        if back == "excess_forward_lean":
            errors.append("forward_lean")

        if depth == "shallow":
            errors.append("shallow_depth")

        return errors