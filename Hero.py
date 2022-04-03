import math

import pygame


class Hero:

    def __init__(self, map_position, screen_position):

        self.map_position = map_position
        self.screen_position = screen_position
        self.angle = 0
        self.image = pygame.image.load("assets/hero.png")

        # self.move_direction = "left"

    def set_angle(self):
        center = self.screen_position.x + self.image.get_size()[0] / 2, self.screen_position.y + self.image.get_size()[
            1] / 2
        distance = math.dist(pygame.mouse.get_pos(), center)
        if distance > 1:
            self.angle = math.degrees(math.acos((center[1] - pygame.mouse.get_pos()[1]) / distance))
            if center[0] < pygame.mouse.get_pos()[0]:
                self.angle = 360.0 - self.angle

    def rot_center(self):
        """rotate an image while keeping its center and size"""

        orig_rect = self.image.get_rect()
        rot_image = pygame.transform.rotate(self.image, self.angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
