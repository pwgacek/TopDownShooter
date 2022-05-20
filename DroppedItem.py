import pygame
from pygame import Vector2
from enum import Enum, auto, unique


@unique
class DroppedItemType(Enum):
    FirstAidKit = auto()
    AmmoPack = auto()
    ShotgunShells = auto()
    Grenades = auto()


def load_images():
    images = list()
    images.append(pygame.image.load("assets/first_aid_kit.png"))
    images.append(pygame.image.load("assets/ammo_pack.png"))
    images.append(pygame.image.load("assets/dropped_shotgun_shells.png"))
    images.append(pygame.image.load("assets/dropped_grenades.png"))

    return images


class DroppedItem:
    __images = load_images()

    def __init__(self, map_position, item_type):
        self.__image = self.choose_image(item_type)
        self.__size = Vector2(self.__image.get_size())
        self.__type = item_type
        self.__map_position = Vector2(map_position.x - self.__image.get_size()[0] // 2,
                                      map_position.y - self.__image.get_size()[1] // 2)

    @classmethod
    def choose_image(cls, item_type):
        return cls.__images[item_type.value - 1]

    def get_image(self):
        return self.__image

    def get_screen_position(self, camera_position):
        return pygame.Vector2(self.__map_position.x - camera_position.x, self.__map_position.y - camera_position.y)

    def get_map_position(self):
        return self.__map_position

    def get_size(self):
        return self.__size

    def get_type(self):
        return self.__type
