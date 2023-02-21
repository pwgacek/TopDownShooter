import math
import random

import pygame
from pygame.math import Vector2
from time import time
from random import randint
from src.aggregates.DroppedItem import DroppedItem
from src.aggregates.DroppedItem import DroppedItemType
from src.utilities.Utils import get_distance, center_map_position, generate_images


class Monster:
    __image = pygame.image.load("../assets/monster1.png")
    __images = generate_images(__image)
    __size = Vector2(__image.get_size())

    def __init__(self, map_position):
        self.__map_position = map_position
        self.__angle = 0
        self.__hp = randint(2, 4)
        self.__shot_time = 0
        self.__last_attack = 0
        self.__speed_ratio = float(randint(10, 12)) / 10

    def get_unit_vector(self, a=None):
        """returns angle converted to unit vector"""
        if a is None:
            a = self.__angle
        x = math.sin(math.radians(a - 180))
        y = math.cos(math.radians(a - 180))

        return Vector2(x, y)

    def update_angle(self, hero):
        """sets value of self.__angle in accordance with hero position"""

        distance = get_distance(hero, self)
        if distance > 1:
            hero_center = center_map_position(hero)
            my_center = center_map_position(self)
            self.__angle = math.degrees(math.acos((my_center.y - hero_center.y) / distance))
            if my_center[0] < hero_center[0]:
                self.__angle = 360.0 - self.__angle

    def hurt(self, shot_time, value):
        self.__shot_time = shot_time
        self.__hp -= value

    def reset_shot_time(self):
        self.__shot_time = 0

    def attack(self):
        self.__last_attack = time()

    def drop_item(self):
        shift = Monster.__size.x // 2
        pos = Vector2(self.__map_position.x + shift, self.__map_position.y + shift)

        random_type = random.choices([t for t in DroppedItemType] + [None], weights=[1, 13, 6, 2, 78], k=1)[0]

        if random_type is None:
            return random_type

        return DroppedItem(pos, random_type)

    @classmethod
    @property
    def size(cls):
        return cls.__size

    @property
    def angle(self):
        return self.__angle

    @property
    def map_position(self):
        return self.__map_position

    @property
    def rotated_image(self):
        """ returns rotated  image while keeping its center and size"""
        return self.__images[int(self.__angle)]

    @property
    def hp(self):
        return self.__hp

    @property
    def shot_time(self):
        return self.__shot_time

    @property
    def last_attack(self):
        return self.__last_attack

    @property
    def speed_ratio(self):
        return self.__speed_ratio
