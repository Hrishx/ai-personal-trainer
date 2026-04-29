class RepAnalyzer:

    def __init__(self):

        self.rep_reports = []

    def analyze_rep(self, rep_data):

        rep = rep_data["rep"]
        score = rep_data["quality_score"]
        knee = rep_data["knee"]
        back = rep_data["back"]
        depth = rep_data["depth"]
        fatigue = rep_data["fatigue"]

        issues = []

        # -------------------------
        # Knee
        # -------------------------

        if knee == "moderate_valgus":
            issues.append("knee collapse")

        elif knee == "mild_valgus":
            issues.append("slight knee valgus")

        # -------------------------
        # Back
        # -------------------------

        if back == "excess_forward_lean":
            issues.append("forward lean")

        elif back == "slight_forward_lean":
            issues.append("slight forward lean")

        # -------------------------
        # Depth
        # -------------------------

        if depth == "shallow":
            issues.append("shallow squat")

        # -------------------------
        # Fatigue
        # -------------------------

        if fatigue == "fatigue_increasing":
            issues.append("fatigue increasing")

        # -------------------------
        # Build report
        # -------------------------

        if not issues:
            report = f"Rep {rep}: Excellent form and control."

        else:
            issue_text = ", ".join(issues)
            report = f"Rep {rep}: {issue_text}."

        self.rep_reports.append(report)

        return report

    def get_rep_reports(self):

        return self.rep_reports