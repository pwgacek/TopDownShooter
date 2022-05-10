import math
import pygame
from pygame.math import Vector2


class Hero:

    def __init__(self, map_position, screen_size):

        self.__map_position = map_position
        self.__image = pygame.image.load("assets/hero2.2.png")
        self.__size = Vector2(self.__image.get_size())
        self.__angle = 0
        self.__screen_position = Vector2(screen_size.x / 2 - self.get_size().x / 2,
                                         screen_size.y / 2 - self.get_size().y / 2)
        self.__bullets_in_the_chamber = 8
        self.__no_ammo_packs = 20
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

    def get_no_ammo_packs(self):
        return self.__no_ammo_packs

    def change_no_ammo_packs(self, num):
        self.__no_ammo_packs += num

    def get_no_ammo(self):
        return self.__no_ammo_packs * 8 + self.__bullets_in_the_chamber

    def hurt(self):
        pass
        #self.__hp -= 1

    def get_hp(self):
        return self.__hp

    def get_max_hp(self):
        return self.__max_hp

    def heal(self):
        self.__hp = self.__max_hp

    def get_size(self):
        return self.__size
