import pygame
from pygame import Vector2
from enum import Enum, auto, unique


@unique
class DroppedItemType(Enum):
    FirstAidKit = auto()
    AmmoPack = auto()
    ShotgunShells = auto()
    Grenades = auto()


def _load_images():
    images = list()
    images.append(pygame.image.load("../assets/first_aid_kit.png"))
    images.append(pygame.image.load("../assets/ammo_pack.png"))
    images.append(pygame.image.load("../assets/dropped_shotgun_shells.png"))
    images.append(pygame.image.load("../assets/dropped_grenades.png"))

    return images


class DroppedItem:
    __images = _load_images()

    def __init__(self, map_position, item_type):
        self.__image = self.choose_image(item_type)
        self.__size = Vector2(self.__image.get_size())
        self.__type = item_type
        self.__map_position = Vector2(map_position.x - self.__image.get_size()[0] // 2,
                                      map_position.y - self.__image.get_size()[1] // 2)

    @classmethod
    def choose_image(cls, item_type):
        return cls.__images[item_type.value - 1]

    @property
    def size(self):
        return self.__size

    @property
    def image(self):
        return self.__image

    @property
    def map_position(self):
        return self.__map_position

    @property
    def type(self):
        return self.__type
