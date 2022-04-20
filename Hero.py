import math
import pygame
from pygame.math import Vector2


class Hero:

    def __init__(self, map_position, screen_size):

        self.__map_position = map_position
        self.__image = pygame.image.load("assets/hero2.2.png")
        self.__angle = 0
        self.__screen_position = Vector2(screen_size.x / 2 - self.__image.get_size()[0] / 2,
                                         screen_size.y / 2 - self.__image.get_size()[1] / 2)
        self.__bullets = 8

    def set_angle(self):
        """sets value of self.__angle in accordance with mouse position"""

        center = self.__screen_position.x + self.__image.get_size()[0] / 2,\
                 self.__screen_position.y + self.__image.get_size()[1] / 2
        distance = math.dist(pygame.mouse.get_pos(), center)
        if distance > 1:
            self.__angle = math.degrees(math.acos((center[1] - pygame.mouse.get_pos()[1]) / distance))
            if center[0] < pygame.mouse.get_pos()[0]:
                self.__angle = 360.0 - self.__angle

    def get_rotated_image(self):
        """ returns rotated  image while keeping its center and size"""

        orig_rect = self.__image.get_rect()
        rot_image = pygame.transform.rotate(self.__image, self.__angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def get_image(self):
        return self.__image

    def get_screen_position(self):
        return self.__screen_position

    def get_map_position(self):
        return self.__map_position

    def get_angle(self):
        return self.__angle

    def get_ammo(self):
        return self.__bullets

    def set_ammo(self, x):
        self.__bullets = x
