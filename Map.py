import pygame
import math

from Hero import Hero
from pygame.math import Vector2


class Map:
    def __init__(self, screen_size):
        self.__width = 2000
        self.__height = 2000
        self.__screen_size = screen_size
        self.__image = pygame.image.load("assets/background2.jpg")
        self.__hero = Hero(Vector2(self.__width / 2, self.__height / 2), self.__screen_size)

    def move_hero(self, move_direction_flags, fps):
        move_speed = 0.3*fps/3

        if (move_direction_flags["down"] and move_direction_flags["up"]) or \
                not (move_direction_flags["down"] or move_direction_flags["up"]):
            change_y = 0
        elif move_direction_flags["down"]:
            change_y = move_speed
        else:
            change_y = -move_speed

        if (move_direction_flags["left"] and move_direction_flags["right"]) or \
                not (move_direction_flags["left"] or move_direction_flags["right"]):
            change_x = 0
        elif move_direction_flags["left"]:
            change_x = -move_speed
        else:
            change_x = move_speed

        destination_x = self.__hero.get_map_position().x + change_x + self.__hero.get_image().get_size()[0] / 2
        destination_y = self.__hero.get_map_position().y + change_y + self.__hero.get_image().get_size()[1] / 2

        """maintain speed when moving diagonally"""
        if change_x and change_y and self.__can_move_to_y(destination_y) and self.__can_move_to_x(destination_x):
            change_x /= math.sqrt(2)
            change_y /= math.sqrt(2)

        """change position if possible"""
        if self.__can_move_to_x(destination_x):
            self.__hero.get_map_position().x += change_x
        if self.__can_move_to_y(destination_y):
            self.__hero.get_map_position().y += change_y

        self.__hero.set_angle()

    def get_camera_position(self):
        """get position of rectangle (cut out of background image) which will be shown on the screen"""
        camera_x = self.__hero.get_map_position().x - self.__hero.get_screen_position().x
        camera_y = self.__hero.get_map_position().y - self.__hero.get_screen_position().y
        return camera_x, camera_y

    def __can_move_to_x(self, x):
        return self.__screen_size.x / 2 < x < self.__width - self.__screen_size.x / 2

    def __can_move_to_y(self, y):
        return self.__screen_size.y / 2 < y < self.__height - self.__screen_size.y / 2

    def get_image(self):
        return self.__image

    def get_hero(self):
        return self.__hero
