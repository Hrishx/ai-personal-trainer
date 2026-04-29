class FeedbackEngine:

    def generate_feedback(self, biomech_data, exercise_rules):
        feedback = []

        knee_angle = biomech_data["knee_angle"]
        back_angle = biomech_data["back_angle"]
        knee_valgus = biomech_data["knee_valgus"]

        # Depth feedback
        if knee_angle > exercise_rules["ideal_knee_angle_max"]:
            feedback.append("Go deeper. Bend your knees more.")

        elif knee_angle < exercise_rules["ideal_knee_angle_min"]:
            feedback.append("Do not go too low. Maintain control.")

        else:
            feedback.append("Good squat depth.")

        # Knee valgus correction
        if knee_valgus:
            feedback.append(
                "Push your knees outward. Activate your gluteus medius."
            )

        # Back angle correction
        if back_angle < 70:
            feedback.append(
                "Keep your chest up. Engage your core and posterior chain."
            )

        # Muscle activation cue
        feedback.append(
            "You should primarily feel this in your quadriceps and glutes."
        )

        return feedback