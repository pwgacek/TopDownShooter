import math
import pygame
from pygame.math import Vector2
from src.aggregates.DroppedItem import DroppedItemType
from src.utilities.Utils import generate_images
from src.aggregates.Weapon import WeaponType, Weapons


class Hero:

    def __init__(self, map_position, screen_size):

        self.__map_position = map_position
        self.__images = generate_images(pygame.image.load("assets/hero2.2.png"))
        self.__size = Vector2(self.__images[0].get_size())
        self.__angle = 0
        self.__screen_position = Vector2(screen_size.x / 2 - self.size.x / 2,
                                         screen_size.y / 2 - self.size.y / 2)
        self.__weapons = Weapons()
        self.__max_hp = 5
        self.__hp = 5

    def update_angle(self):
        """sets value of self.__angle in accordance with mouse position"""

        screen_center = self.__screen_position.x + self.size.x / 2, \
                        self.__screen_position.y + self.size.y / 2

        distance = math.dist(pygame.mouse.get_pos(), screen_center)
        if distance > 1:
            self.__angle = math.degrees(math.acos((screen_center[1] - pygame.mouse.get_pos()[1]) / distance))
            if screen_center[0] < pygame.mouse.get_pos()[0]:
                self.__angle = 360.0 - self.angle

    def pick_up_dropped_item(self, item):
        if item.type == DroppedItemType.FirstAidKit:
            self.__hp = self.__max_hp
        elif item.type == DroppedItemType.AmmoPack:
            self.__weapons.updated_ammo_packs(WeaponType.pistol, 2)
        elif item.type == DroppedItemType.ShotgunShells:
            self.__weapons.updated_ammo_packs(WeaponType.shotgun, 2)
        elif item.type == DroppedItemType.Grenades:
            self.__weapons.updated_ammo_packs(WeaponType.grenade, 1)

    def get_no_ammo(self):
        if self.__weapons.current_weapon == WeaponType.pistol:
            return self.__weapons.packs * 8 + self.__weapons.in_chamber
        elif self.__weapons.current_weapon == WeaponType.grenade:
            return self.__weapons.packs * 3 + self.__weapons.in_chamber
        elif self.__weapons.current_weapon == WeaponType.shotgun:
            return self.__weapons.packs * 4 + self.__weapons.in_chamber

    def hurt(self, value):
        self.__hp -= value

    def heal(self):
        self.__hp = self.__max_hp

    @property
    def weapons(self):
        return self.__weapons

    @property
    def size(self):
        return self.__size

    @property
    def angle(self):
        return self.__angle

    @property
    def map_position(self):
        return self.__map_position

    @property
    def screen_position(self):
        return self.__screen_position

    @property
    def rotated_image(self):
        """ returns rotated  image while keeping its center and size"""
        return self.__images[int(self.__angle)]

    @property
    def hp(self):
        return self.__hp

    @property
    def max_hp(self):
        return self.__max_hp
