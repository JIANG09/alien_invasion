class Settings():
    """store all the set classes in alien_invasion"""

    def __init__(self):
        """static settings for initiating game"""
        # screen set
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # ship setting
        self.ship_limit = 3

        # bullets set
        self.bullet_width = 3
        self.bullet_height =15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3 

        # alien set
        self.fleet_drop_speed = 12

        # which speed is used to speed up the game 
        self.speedup_scale = 1.4
        # speed up the points of aliens
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """initialize the settings that is changing in the game"""
        self.ship_speed_factor = 4
        self.bullet_speed_factor = 4
        self.alien_speed_factor = 3

        # fleet_direction = 1: moving right; fleet_direction = -1: moving left
        self.fleet_direction = 1

        # score
        self.alien_points = 50


    def increase_speed(self):
        """settings for increasing speed and alien points"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

        

