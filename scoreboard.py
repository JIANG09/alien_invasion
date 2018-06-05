import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """class for showing scores"""

    def __init__(self, ai_settings, screen, stats):
        """initializing attributes of scoreboard"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # font for display score
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 47)

        # prepare initializing score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """render score into a image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # scoreboard on the right corner of the image
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        """render the highes score into a image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                    self.text_color, self.ai_settings.bg_color)

        # highest scoreboard in the middle of the top
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        """render level into an image"""
        self.level_image = self.font.render(str(self.stats.level), True,
                                self.text_color, self.ai_settings.bg_color)

        #  under the scoreboard
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_ships(self):
        """how many ships are left"""
        self.ships = Group()
        for ship_num in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_num * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def show_score(self):
        """draw score on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # draw the ships
        self.ships.draw(self.screen)
