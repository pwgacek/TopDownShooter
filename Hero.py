import math
import pygame
from pygame.math import Vector2
from DroppedItem import DroppedItemType


class Hero:

    def __init__(self, map_position, screen_size):

        self.__map_position = map_position
        self.__image = pygame.image.load("assets/hero2.2.png")
        self.__size = Vector2(self.__image.get_size())
        self.__angle = 0
        self.__screen_position = Vector2(screen_size.x / 2 - self.get_size().x / 2,
                                         screen_size.y / 2 - self.get_size().y / 2)
        self.__bullets_in_the_chamber = 8
        self.__grenades_in_pocket = 3
        self.__shotgun_shells_in_chamber = 4
        self.__no_ammo_packs = 20
        self.__no_grenade_packs = 3
        self.__no_shotgun_shells_packs = 10
        self.__max_hp = 5
        self.__hp = 5

    def set_angle(self):
        """sets value of self.__angle in accordance with mouse position"""

        center = self.__screen_position.x + self.get_size().x / 2, \
                 self.__screen_position.y + self.get_size().y / 2
        distance = math.dist(pygame.mouse.get_pos(), center)
        if distance > 1:
            self.__angle = math.degrees(math.acos((center[1] - pygame.mouse.get_pos()[1]) / distance))
            if center[0] < pygame.mouse.get_pos()[0]:
                self.__angle = 360.0 - self.__angle

    def get_rotated_image(self):
        """ returns rotated  image while keeping its center and size"""

        orig_rect = self.__image.get_rect()
        rot_image = pygame.transform.rotate(self.__image, self.__angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def pick_up_dropped_item(self, item):
        if item.get_type() == DroppedItemType.FirstAidKit:
            self.__hp = self.__max_hp
        elif item.get_type() == DroppedItemType.AmmoPack:
            self.change_no_ammo_packs(2)
        elif item.get_type() == DroppedItemType.ShotgunShells:
            self.change_no_shotgun_packs(2)
        elif item.get_type() == DroppedItemType.Grenades:
            self.change_no_grenades_packs(1)

    def get_image(self):
        return self.__image

    def get_screen_position(self):
        return self.__screen_position

    def get_map_position(self):
        return self.__map_position

    def get_angle(self):
        return self.__angle

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

    def get_no_granades(self):
        return self.__no_grenade_packs * 3 + self.__grenades_in_pocket

    def get_no_shotgun_shells(self):
        return self.__no_shotgun_shells_packs * 4 + self.__shotgun_shells_in_chamber

    def hurt(self, value):
        self.__hp -= value

    def get_hp(self):
        return self.__hp

    def get_max_hp(self):
        return self.__max_hp

    def heal(self):
        self.__hp = self.__max_hp

    def get_size(self):
        return self.__size
