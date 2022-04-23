import random

import pygame
from Map import Map
from pygame.math import Vector2


class GameEngine:
    def __init__(self):
        pygame.init()
        self.__width = 800
        self.__height = 600
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__map = Map(Vector2(self.__screen.get_size()))
        pygame.display.set_caption("Top-Down Shooter")

    def run(self):
        running = True
        fps = 60
        fps_clock = pygame.time.Clock()

        """set true if key is pressed"""
        move_direction_flags = {"up": False, "down": False, "left": False, "right": False}
        # for i in range(20):
        #     self.__map.add_monster()

        """main game loop"""
        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and self.__map.get_hero().get_ammo() > 0:
                    self.__map.add_bullet()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        self.__map.get_hero().set_ammo(8)

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

            self.__map.move_hero(move_direction_flags, fps * 0.1)
            self.__map.move_monsters(fps * 0.02)

            camera_position = self.__map.get_camera_position()

            """clears screen"""
            self.__screen.fill((0, 102, 0))

            """shows hero on the screen"""
            self.__screen.blit(self.__map.get_hero().get_rotated_image(), self.__map.get_hero().get_screen_position())

            """shows monsters on the screen"""
            for monster in self.__map.get_monsters():
                if self.__map.is_on_screen(monster, self.__map.get_camera_position()):
                    self.__screen.blit(monster.get_rotated_image(),
                                       monster.get_screen_position(self.__map.get_camera_position()))

            # """shows map elements on screen"""
            # for elem in self.__map.get_array_elements_on_screen():
            #     v, num = elem
            #     shift = (self.__map.get_tree_image().get_size()[0] - self.__map.get_chunk_size()) / 2
            #     self.__screen.blit(self.__map.get_tree_surface(num),
            #                         Vector2(v.x * self.__map.get_chunk_size() - shift - self.__map.get_camera_position().x,
            #                                 v.y * self.__map.get_chunk_size() - shift - self.__map.get_camera_position().y))

            """shows bullets, their movement and removal"""

            for bullet in self.__map.get_bullets():
                if self.__map.is_on_screen(bullet, self.__map.get_camera_position()):
                    self.__screen.blit(bullet.get_image(),
                                       bullet.get_screen_position(self.__map.get_camera_position()))

            """shows map on the screen"""
            self.__screen.blit(self.__map.get_background(), Vector2(0, 0),
                               pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))

            self.__map.show_ammo2(self.__screen)

            self.__map.move_bullets()
            self.__map.remove_bullets()

            pygame.display.update()
            fps_clock.tick(fps)
