import pygame


class Hero:

    def __init__(self, map_position, screen_position):

        self.map_position = map_position
        self.screen_position = screen_position
        self.aim_direction = 0
        self.image = pygame.image.load("assets/hero.png")
        #self.move_direction = "left"
