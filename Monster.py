import math

import pygame
from pygame.math import Vector2
from time import time


class Monster:
    def __init__(self, map_position):
        self.__map_position = map_position
        self.__angle = 0
        self.__image = pygame.image.load("assets/monster1.png")
        self.__hp = 3
        self.__shot_time = 0
        self.__last_attack = 0

    def __eq__(self, other):
        return self is other

    def get_map_position(self):
        return self.__map_position

    def get_angle(self):
        return self.__angle

    def get_image(self):
        return self.__image

    def get_unit_vector(self, a=None):
        """returns angle converted to unit vector"""
        if a is None:
            a = self.__angle
        x = math.sin(math.radians(a - 180))
        y = math.cos(math.radians(a - 180))

        return Vector2(x, y)

    def get_rotated_image(self):
        """ returns rotated  image while keeping its center and size"""

        orig_rect = self.__image.get_rect()
        rot_image = pygame.transform.rotate(self.__image, self.__angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def get_screen_position(self, camera_position):
        return Vector2(self.__map_position.x - camera_position.x, self.__map_position.y - camera_position.y)

    def set_angle(self, hero_map_position):
        """sets value of self.__angle in accordance with hero position"""

        hero_center = Vector2(hero_map_position.x + self.__image.get_size()[0] / 2,
                              hero_map_position.y + self.__image.get_size()[1] / 2)
        my_center = Vector2(self.__map_position.x + self.__image.get_size()[0] / 2,
                            self.__map_position.y + self.__image.get_size()[1] / 2)
        distance = math.dist(hero_center, my_center)
        if distance > 1:
            self.__angle = math.degrees(math.acos((my_center.y - hero_center.y) / distance))
            if my_center[0] < hero_center[0]:
                self.__angle = 360.0 - self.__angle

    def shot(self, time):
        self.__shot_time = time
        self.__hp -= 1
        return self.__hp

    def get_time(self):
        return self.__shot_time

    def set_time(self):
        self.__shot_time = 0

    def attack(self):
        self.__last_attack = time()

    def get_last_attack(self):
        return self.__last_attack