import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """a class for bullets from ship"""

    def __init__(self, ai_settings, screen, ship):
        """create a bullet object where the ship is"""
        super(Bullet, self).__init__()
        self.screen = screen

        # set a rect for bullet at(0, 0) and replace it right
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the bullet position with float
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor


    def update(self):
        """move bullet upwards"""
        # update the float value of bullet position
        self.y -= self.speed_factor
        # update the bullet position
        self.rect.y = self.y


    def draw_bullet(self):
        """draw the bullet on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
