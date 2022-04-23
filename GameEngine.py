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
        monster_clock = pygame.time.Clock()
        delta = 0
        """set true if key is pressed"""
        move_direction_flags = {"up": False, "down": False, "left": False, "right": False}

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

            """maintain number of monsters """
            self.__map.keep_no_monsters()

            """increase number of monsters every 10 seconds"""
            delta += monster_clock.tick()
            if delta > 10000:
                self.__map.increase_min_no_monsters(1)
                delta = 0
            """move all map elements"""
            self.move_map_elements(move_direction_flags, fps)
            """clears screen"""
            self.__screen.fill((0, 102, 0))
            """draws  map elements and ammo """
            self.draw_map(self.__map.get_camera_position())

            pygame.display.update()
            fps_clock.tick(fps)

    def move_map_elements(self, move_direction_flags, fps):
        self.__map.move_hero(move_direction_flags, fps * 0.1)
        self.__map.move_monsters(fps * 0.02)
        self.__map.move_bullets()

    def draw_map(self, camera_position):
        shift = (self.__map.get_tree_size()[0] - self.__map.get_chunk_size()) // 2

        screen_shift_x = camera_position.x - int(
            self.__map.get_camera_position().x // self.__width) * self.__width
        screen_shift_y = camera_position.y - int(
            self.__map.get_camera_position().y // self.__height) * self.__height

        """show grass"""

        arr_x = int(self.__map.get_camera_position().x // self.__width)
        arr_y = int(self.__map.get_camera_position().y // self.__height)

        self.__screen.blit(self.__map.get_grassland()[arr_x][arr_y], Vector2(0, 0),
                           pygame.Rect(screen_shift_x, screen_shift_y, self.__width - screen_shift_x, self.__height - screen_shift_y))
        self.__screen.blit(self.__map.get_grassland()[arr_x + 1][arr_y], Vector2(self.__width - screen_shift_x, 0),
                           pygame.Rect(0, screen_shift_y, screen_shift_x, self.__height - screen_shift_y))
        self.__screen.blit(self.__map.get_grassland()[arr_x][arr_y + 1], Vector2(0, self.__height - screen_shift_y),
                           pygame.Rect(screen_shift_x, 0, self.__width - screen_shift_x, screen_shift_y))
        self.__screen.blit(self.__map.get_grassland()[arr_x + 1][arr_y + 1],
                           Vector2(self.__width - screen_shift_x, self.__height - screen_shift_y),
                           pygame.Rect(0, 0, screen_shift_x, screen_shift_y))

        """shows hero on the screen"""
        self.__screen.blit(self.__map.get_hero().get_rotated_image(), self.__map.get_hero().get_screen_position())

        """shows monsters on the screen"""
        for monster in self.__map.get_monsters():
            if self.__map.is_on_screen(monster, self.__map.get_camera_position()):
                self.__screen.blit(monster.get_rotated_image(),
                                   monster.get_screen_position(self.__map.get_camera_position()))

        """shows bullets, their movement and removal"""

        for bullet in self.__map.get_bullets():
            if self.__map.is_on_screen(bullet, self.__map.get_camera_position()):
                self.__screen.blit(bullet.get_image(),
                                   bullet.get_screen_position(self.__map.get_camera_position()))

        """shows map on the screen"""
        self.__screen.blit(self.__map.get_background()[arr_x][arr_y], Vector2(-shift, -shift),
                           pygame.Rect(screen_shift_x, screen_shift_y, self.__width -screen_shift_x + shift, self.__height - screen_shift_y +shift))
        self.__screen.blit(self.__map.get_background()[arr_x+1][arr_y], Vector2(self.__width-screen_shift_x-shift,-shift),
                           pygame.Rect(0, screen_shift_y, screen_shift_x + shift, self.__height - screen_shift_y +shift))
        self.__screen.blit(self.__map.get_background()[arr_x][arr_y+1], Vector2(-shift, self.__height-screen_shift_y-shift),
                           pygame.Rect(screen_shift_x, 0, self.__width -screen_shift_x + shift, screen_shift_y + shift))
        self.__screen.blit(self.__map.get_background()[arr_x+1][arr_y+1], Vector2(self.__width - screen_shift_x - shift,
                                                                                  self.__height - screen_shift_y - shift),
                           pygame.Rect(0, 0, screen_shift_x + shift, screen_shift_y + shift))
        "show remaining ammo"
        ammo_shift = 20
        for i in range(self.__map.get_hero().get_ammo()):
            self.__screen.blit(self.__map.get_bullet_image(), (ammo_shift, 520))
            ammo_shift += self.__map.get_bullet_image().get_size()[0]
