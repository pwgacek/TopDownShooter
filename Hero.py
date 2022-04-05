import math

import pygame


class Hero:

    def __init__(self, map_position, screen_position):

        self.__map_position = map_position
        self.__screen_position = screen_position
        self.__angle = 0
        self.__image = pygame.image.load("assets/hero.png")
        self.__dir = {"up": False, "down": False, "left": False, "right": False}

        # self.move_direction = "left"

    def set_angle(self):
        center = self.__screen_position.x + self.__image.get_size()[0] / 2, self.__screen_position.y + \
                 self.__image.get_size()[
                     1] / 2
        distance = math.dist(pygame.mouse.get_pos(), center)
        if distance > 1:
            self.__angle = math.degrees(math.acos((center[1] - pygame.mouse.get_pos()[1]) / distance))
            if center[0] < pygame.mouse.get_pos()[0]:
                self.__angle = 360.0 - self.__angle

    def rot_center(self):
        """rotate an image while keeping its center and size"""

        orig_rect = self.__image.get_rect()
        rot_image = pygame.transform.rotate(self.__image, self.__angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def get_dir(self):
        return self.__dir

    def get_image(self):
        return self.__image

    def get_screen_pos(self):
        return self.__screen_position

    def get_map_pos(self):
        return self.__map_position
