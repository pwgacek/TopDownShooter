import pygame
from pygame.math import Vector2
import math


class Grenade:
    __image = pygame.image.load("assets/grenade.png")
    __size = Vector2(__image.get_size())

    def __init__(self, map_position, angle, create_time):
        self.__angle = angle
        self.__map_position = Vector2(map_position.x - self.__size.x / 2 + math.cos(math.radians(angle - 14)) * 50,
                                      map_position.y - self.__size.y / 2 - math.sin(math.radians(angle - 14)) * 50)
        self.__create_time = create_time

    def move(self, speed):
        """ moves current grenade on  map"""

        x1 = math.cos(math.radians(self.__angle))
        y1 = math.sin(math.radians(self.__angle))
        a = self.__map_position.x + x1 * speed
        b = self.__map_position.y - y1 * speed
        self.__map_position = Vector2(a, b)

    @classmethod
    @property
    def image(cls):
        return cls.__image

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
    def create_time(self):
        return self.__create_time
