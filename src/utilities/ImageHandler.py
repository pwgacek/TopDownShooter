import pygame
from src.utilities.Utils import get_rotated_image
from src.utilities.MapGenerator import generate_borders, generate_grass, generate_map_elements


class ImageHandler:
    def __init__(self, chunk_size, map_size, array):
        self.__bullet_image = pygame.image.load("assets/ammo1.png")
        self.__grenade_image = pygame.image.load("assets/grenade_ico.png")
        self.__shell_image = pygame.image.load("assets/shotgun_shell.png")
        self.__reload_image = pygame.image.load("assets/reload.png")
        self.__ammo_image = pygame.image.load("assets/ammo_pack2.png")
        self.__grenades_image = pygame.image.load("assets/many_granedesv2.png")
        self.__shotgun_shells_image = pygame.image.load("assets/shotgun_shellsv2.png")

        self.__borders = generate_borders(chunk_size, map_size, array)
        self.__grassland = generate_grass(chunk_size, map_size, array)
        self.__map_elements = generate_map_elements(chunk_size, map_size, array)

        self.__reload_angle = 0
        self.reload_time = 0

    @property
    def bullet_image(self):
        return self.__bullet_image

    @property
    def ammo_image(self):
        return self.__ammo_image

    @property
    def grenade_image(self):
        return self.__grenade_image

    @property
    def grenades_image(self):
        return self.__grenades_image

    @property
    def shell_image(self):
        return self.__shell_image

    @property
    def shotgun_shells_image(self):
        return self.__shotgun_shells_image

    @property
    def rotated_reload_image(self):
        """ returns rotated  image while keeping its center and size"""

        rot_image = get_rotated_image(self.__reload_image, self.__reload_angle)
        self.__reload_angle += -5
        return rot_image

    @property
    def borders_image(self):
        return self.__borders

    @property
    def grassland_image(self):
        return self.__grassland

    @property
    def map_elements_image(self):
        return self.__map_elements
