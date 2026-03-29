class UserTracker:
    def __init__(self):
        self.user_data = {}

    def track_behavior(self, user_id, behavior):
        # Track user behavior
        if user_id not in self.user_data:
            self.user_data[user_id] = {'behaviors': [], 'preferences': {}, 'interactions': []}
        self.user_data[user_id]['behaviors'].append(behavior)

    def set_preferences(self, user_id, preferences):
        # Set user preferences
        if user_id not in self.user_data:
            self.user_data[user_id] = {'behaviors': [], 'preferences': {}, 'interactions': []}
        self.user_data[user_id]['preferences'] = preferences

    def track_interaction(self, user_id, interaction):
        # Track user interaction
        if user_id not in self.user_data:
            self.user_data[user_id] = {'behaviors': [], 'preferences': {}, 'interactions': []}
        self.user_data[user_id]['interactions'].append(interaction)

    def generate_user_profiles(self):
        # Generate user profiles based on tracked data
        return self.user_data
