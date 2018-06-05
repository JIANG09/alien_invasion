class GameStats():
    """follow the statistics info in the game"""

    def __init__(self, ai_settings):
        """initiate stats"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # game is active when starting
        self.game_active = False

        # not to reset highest score at any time
        self.high_score = 0 

    def reset_stats(self):
        """initiate the stats that may change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
