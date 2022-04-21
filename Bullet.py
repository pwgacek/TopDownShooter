import pygame
from pygame.math import Vector2
import math


class Bullet:
    def __init__(self, map_position, angle, screen_size):
        self.__map_position = map_position
        self.__angle = angle
        self.__image = pygame.transform.rotate(pygame.image.load("assets/bullet.png"), angle - 90)
        self.__screen_position = Vector2(
            screen_size.x / 2 - self.__image.get_size()[0] / 2 + math.cos(math.radians(angle - 14)) * 50,
            screen_size.y / 2 - self.__image.get_size()[1] / 2 - math.sin(math.radians(angle - 14)) * 50)

    def update_screen_pos(self, x, y):
        """ updates screen position of current bullet """
        self.__screen_position = Vector2(self.__screen_position[0] - x, self.__screen_position[1] - y)

    def move(self):
        """ moves current bullet on both screen and whole map"""
        speed = 15
        x1 = math.cos(math.radians(self.__angle))
        y1 = math.sin(math.radians(self.__angle))
        x = self.__screen_position[0] + x1 * speed
        y = self.__screen_position[1] - y1 * speed
        a = self.__map_position[0] + x1 * speed
        b = self.__map_position[0] - y1 * speed
        self.__screen_position = Vector2(x, y)
        self.__map_position = Vector2(a, b)

    def get_screen_position(self):
        return self.__screen_position

    def get_map_position(self):
        return self.__map_position

    def get_angle(self):
        return self.__angle

    def get_image(self):
        return self.__image
