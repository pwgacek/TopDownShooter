import pygame
from pygame import Vector2


class GrenadePack:
    """To Set Img"""
    __image = pygame.image.load("assets/ammo_pack.png")
    __size = Vector2(__image.get_size())

    def __init__(self, map_position):
        self.__map_position = Vector2(map_position.x - self.__image.get_size()[0] // 2,
                                      map_position.y - self.__image.get_size()[1] // 2)

    @classmethod
    def get_image(cls):
        return cls.__image

    def get_screen_position(self, camera_position):
        return pygame.Vector2(self.__map_position.x - camera_position.x, self.__map_position.y - camera_position.y)

    def get_map_position(self):
        return self.__map_position

    @classmethod
    def get_size(cls):
        return cls.__size