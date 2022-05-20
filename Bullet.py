import pygame
from pygame.math import Vector2
import math


class Bullet:
    __image = pygame.image.load("assets/bullet.png")
    __size = Vector2(__image.get_size())

    def __init__(self, map_position, angle, hero_size, damage):
        self.__angle = angle
        # self.__image = pygame.transform.rotate(pygame.image.load("assets/bullet.png"), angle - 90)
        self.__map_position = Vector2(
            map_position.x + hero_size.x / 2 - self.get_size().x / 2 + math.cos(
                math.radians(angle - 14)) * 50,
            map_position.y + hero_size.y / 2 - self.get_size().y / 2 - math.sin(
                math.radians(angle - 14)) * 50)
        self.__damage = damage

    def move(self, speed):
        """ moves current bullet on  map"""

        x1 = math.cos(math.radians(self.__angle))
        y1 = math.sin(math.radians(self.__angle))
        a = self.__map_position.x + x1 * speed
        b = self.__map_position.y - y1 * speed
        self.__map_position = Vector2(a, b)

    def get_screen_position(self, camera_position):
        return Vector2(self.__map_position.x - camera_position.x, self.__map_position.y - camera_position.y)

    def get_map_position(self):
        return self.__map_position

    def get_angle(self):
        return self.__angle

    def get_damage(self):
        return self.__damage

    @classmethod
    def get_image(cls):
        return cls.__image

    @classmethod
    def get_size(cls):
        return cls.__size
