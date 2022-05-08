import pygame
from pygame import Vector2


class FirstAidKit:
    __image = None

    def __init__(self, map_position):
        self.__image = pygame.image.load("assets/first_aid_kit.png")
        self.__map_position = Vector2(map_position.x - self.__image.get_size()[0] // 2,
                                      map_position.y - self.__image.get_size()[1] // 2)

    @classmethod
    def get_image(cls):
        return FirstAidKit.__image

    def get_screen_position(self, camera_position):
        return pygame.Vector2(self.__map_position.x - camera_position.x, self.__map_position.y - camera_position.y)

    def get_map_position(self):
        return self.__map_position

    def get_image(self):
        return self.__image
