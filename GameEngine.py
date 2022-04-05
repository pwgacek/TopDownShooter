import pygame
from Map import Map
from pygame.math import Vector2


class GameEngine:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((800, 600))
        self.__map = Map(Vector2(self.__screen.get_size()))
        pygame.display.set_caption("Top-Down Shooter")

    def run(self):
        running = True

        """set true if key is pressed"""
        move_direction_flags = {"up": False, "down": False, "left": False, "right": False}

        """main game loop"""
        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_w:
                        move_direction_flags["up"] = True
                    if event.key == pygame.K_s:
                        move_direction_flags["down"] = True
                    if event.key == pygame.K_a:
                        move_direction_flags["left"] = True
                    if event.key == pygame.K_d:
                        move_direction_flags["right"] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        move_direction_flags["up"] = False
                    if event.key == pygame.K_s:
                        move_direction_flags["down"] = False
                    if event.key == pygame.K_a:
                        move_direction_flags["left"] = False
                    if event.key == pygame.K_d:
                        move_direction_flags["right"] = False

            self.__map.move_hero(move_direction_flags)

            camera_x, camera_y = self.__map.get_camera_position()
            self.__screen.blit(self.__map.get_image(), Vector2(0, 0), pygame.Rect(camera_x, camera_y, 800, 600))
            self.__screen.blit(self.__map.get_hero().get_rotated_image(), self.__map.get_hero().get_screen_position())

            pygame.display.update()
