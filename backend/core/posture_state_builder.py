class PostureStateBuilder:

    def build_state(self, biomech_data):

        knee_offset = biomech_data["knee_offset"]
        back_angle = biomech_data["back_angle"]
        hip_depth = biomech_data["hip_depth"]

        if abs(knee_offset) < 0.02:
            knee_status = "aligned"

        elif abs(knee_offset) < 0.05:
            knee_status = "mild_valgus"

        else:
            knee_status = "moderate_valgus"

        if back_angle >= 75:
            back_status = "neutral"

        elif back_angle >= 65:
            back_status = "slight_forward_lean"

        else:
            back_status = "excess_forward_lean"

        if hip_depth >= 0.1:
            depth_status = "good_depth"

        elif hip_depth >= 0.07:
            depth_status = "moderate_depth"

        else:
            depth_status = "shallow"

        severity = 0

        if knee_status == "moderate_valgus":
            severity += 2

        if back_status == "excess_forward_lean":
            severity += 2

        if depth_status == "shallow":
            severity += 1

        return {
            "knee_status": knee_status,
            "back_status": back_status,
            "depth_status": depth_status,
            "rep_phase": biomech_data["state"],
            "rep_count": biomech_data["rep_count"],
            "severity_score": severity
        }