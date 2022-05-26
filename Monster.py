import math

import pygame
from pygame.math import Vector2
from time import time
from random import randint
from DroppedItem import DroppedItem
from DroppedItem import DroppedItemType


def generate_images(image):
    images = [None for _ in range(360)]
    for angle in range(360):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        images[angle] = rot_image.subsurface(rot_rect).copy()

    return images


class Monster:
    __image = pygame.image.load("assets/monster1.png")
    __images = generate_images(__image)
    __size = Vector2(__image.get_size())

    def __init__(self, map_position):
        self.__map_position = map_position
        self.__angle = 0
        self.__hp = randint(2, 4)
        self.__shot_time = 0
        self.__last_attack = 0
        self.__speed_ratio = float(randint(8, 12)) / 10

    def get_map_position(self):
        return self.__map_position

    def get_angle(self):
        return self.__angle

    @classmethod
    def get_image(cls):
        return cls.__image

    def get_unit_vector(self, a=None):
        """returns angle converted to unit vector"""
        if a is None:
            a = self.__angle
        x = math.sin(math.radians(a - 180))
        y = math.cos(math.radians(a - 180))

        return Vector2(x, y)

    def get_rotated_image(self):
        """ returns rotated  image while keeping its center and size"""
        return self.__images[int(self.__angle)]

    def get_screen_position(self, camera_position):
        return Vector2(self.__map_position.x - camera_position.x, self.__map_position.y - camera_position.y)

    def set_angle(self, hero):
        """sets value of self.__angle in accordance with hero position"""

        hero_center = Vector2(hero.get_map_position().x + hero.get_size().x / 2,
                              hero.get_map_position().y + hero.get_size().y / 2)
        my_center = Vector2(self.__map_position.x + self.__size.x / 2,
                            self.__map_position.y + self.__size.y / 2)

        distance = math.dist(hero_center, my_center)
        if distance > 1:
            self.__angle = math.degrees(math.acos((my_center.y - hero_center.y) / distance))
            if my_center[0] < hero_center[0]:
                self.__angle = 360.0 - self.__angle

    def hurt(self, shot_time, value):
        self.__shot_time = shot_time
        self.__hp -= value

    def get_hp(self):
        return self.__hp

    def get_time(self):
        return self.__shot_time

    def set_time(self):
        self.__shot_time = 0

    def attack(self):
        self.__last_attack = time()

    def get_last_attack(self):
        return self.__last_attack

    def get_speed_ratio(self):
        return self.__speed_ratio

    @classmethod
    def get_size(cls):
        return cls.__size

    def drop_item(self):
        shift = Monster.get_size().x // 2
        pos = Vector2(self.get_map_position().x + shift, self.get_map_position().y + shift)
        r = randint(0, 40)
        item = None
        if r == 0:
            item = DroppedItem(pos, DroppedItemType.FirstAidKit)
        elif r < 8:
            item = DroppedItem(pos, DroppedItemType.AmmoPack)
        elif r < 11:
            item = DroppedItem(pos, DroppedItemType.ShotgunShells)
        elif r < 12:
            item = DroppedItem(pos, DroppedItemType.Grenades)

        return item
