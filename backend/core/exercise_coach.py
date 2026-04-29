class ExerciseCoach:

    def get_intro(self, exercise):

        if exercise == "squat":
            return (
                "Today's exercise is squat. "
                "Target muscles: glutes, quadriceps and core. "
                "Focus on pushing your knees outward and driving through your heels."
            )

        elif exercise == "pushup":
            return (
                "Today's exercise is push up. "
                "Target muscles: chest, triceps and shoulders. "
                "Keep your body straight and engage your core."
            )

        elif exercise == "lunge":
            return (
                "Today's exercise is lunge. "
                "Target muscles: quadriceps, glutes and hamstrings. "
                "Keep your front knee aligned with your toes."
            )

        else:
            return "Get ready for your workout."