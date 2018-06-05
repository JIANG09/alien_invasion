import pygame

def draw_screen(color):
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption('This is screen')
    screen.fill(color)
    pygame.display.flip()


draw_screen((0,0,230))
