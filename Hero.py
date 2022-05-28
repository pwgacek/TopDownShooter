import math
import pygame
from pygame.math import Vector2
from DroppedItem import DroppedItemType
from Utils import generate_images


class Hero:

    def __init__(self, map_position, screen_size):

        self.__map_position = map_position
        self.__images = generate_images(pygame.image.load("assets/hero2.2.png"))
        self.__size = Vector2(self.__images[0].get_size())
        self.__angle = 0
        self.__screen_position = Vector2(screen_size.x / 2 - self.size.x / 2,
                                         screen_size.y / 2 - self.size.y / 2)
        self.__bullets_in_the_chamber = 8
        self.__grenades_in_pocket = 3
        self.__shotgun_shells_in_chamber = 4
        self.__no_ammo_packs = 20
        self.__no_grenade_packs = 3
        self.__no_shotgun_shells_packs = 10
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
            self.change_no_ammo_packs(2)
        elif item.type == DroppedItemType.ShotgunShells:
            self.change_no_shotgun_packs(2)
        elif item.type == DroppedItemType.Grenades:
            self.change_no_grenades_packs(1)

    def get_no_bullets_in_the_chamber(self):
        return self.__bullets_in_the_chamber

    def set_no_bullets_in_the_chamber(self, x):
        self.__bullets_in_the_chamber = x

    def get_no_grenades_in_pocket(self):
        return self.__grenades_in_pocket

    def set_no_grenades_in_pocket(self, x):
        self.__grenades_in_pocket = x

    def get_no_shells_in_chamber(self):
        return self.__shotgun_shells_in_chamber

    def set_no_shells_in_chamber(self, x):
        self.__shotgun_shells_in_chamber = x

    def get_no_ammo_packs(self):
        return self.__no_ammo_packs

    def change_no_ammo_packs(self, num):
        self.__no_ammo_packs += num

    def get_no_grenades_packs(self):
        return self.__no_grenade_packs

    def change_no_grenades_packs(self, x):
        self.__no_grenade_packs += x

    def get_no_shotgun_packs(self):
        return self.__no_shotgun_shells_packs

    def change_no_shotgun_packs(self, x):
        self.__no_shotgun_shells_packs += x

    def get_no_ammo(self, weapon_type):
        if weapon_type == "p":
            return self.__no_ammo_packs * 8 + self.__bullets_in_the_chamber
        elif weapon_type == "g":
            return self.__no_grenade_packs * 3 + self.__grenades_in_pocket
        elif weapon_type == "s":
            return self.__no_shotgun_shells_packs * 4 + self.__shotgun_shells_in_chamber

    def get_no_grenades(self):
        return self.__no_grenade_packs * 3 + self.__grenades_in_pocket

    def get_no_shotgun_shells(self):
        return self.__no_shotgun_shells_packs * 4 + self.__shotgun_shells_in_chamber

    def hurt(self, value):
        self.__hp -= value

    def heal(self):
        self.__hp = self.__max_hp

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
