class UserProfile:

    def __init__(self):

        self.motivation_style = "elite"
        self.emotional_state = "normal"
        self.user_goal = "general_fitness"

    def set_profile(self, style, emotional_state="normal", goal="general_fitness"):

        self.motivation_style = style
        self.emotional_state = emotional_state
        self.user_goal = goal

    def get_profile(self):

        return {
            "motivation_style": self.motivation_style,
            "emotional_state": self.emotional_state,
            "user_goal": self.user_goal
        }