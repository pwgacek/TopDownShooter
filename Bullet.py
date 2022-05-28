import pygame
from pygame.math import Vector2
import math


class Bullet:
    __image = pygame.image.load("assets/bullet.png")
    __size = Vector2(__image.get_size())

    def __init__(self, map_position, angle, damage):
        self.__angle = angle
        self.__map_position = Vector2(map_position.x - self.size.x / 2 + math.cos(math.radians(angle - 14)) * 50,
                                      map_position.y - self.size.y / 2 - math.sin(math.radians(angle - 14)) * 50)
        self.__damage = damage

    def move(self, speed):
        """ moves current bullet on  map"""

        x1 = math.cos(math.radians(self.angle))
        y1 = math.sin(math.radians(self.angle))
        a = self.map_position.x + x1 * speed
        b = self.map_position.y - y1 * speed
        self.__map_position = Vector2(a, b)

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
    def damage(self):
        return self.__damage
