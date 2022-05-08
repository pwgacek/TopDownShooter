from time import time

import pygame
from pygame.math import Vector2

from FirstAidKit import FirstAidKit
from Map import Map


class GameEngine:
    def __init__(self):
        pygame.init()
        self.__width = 800
        self.__height = 600
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__map = Map(Vector2(self.__screen.get_size()))
        self.__font = pygame.font.SysFont('arial', 32, bold=pygame.font.Font.bold)
        pygame.display.set_caption("Top-Down Shooter")

    def run(self):
        running = True
        hero_alive = True
        game_over = True
        fps = 60
        fps_clock = pygame.time.Clock()
        monster_clock = pygame.time.Clock()
        self.set_map(Map(Vector2(self.__screen.get_size())))
        delta = 0
        """set true if key is pressed"""
        move_direction_flags = {"up": False, "down": False, "left": False, "right": False}

        """main game loop"""
        while running and hero_alive:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    game_over = False

                if event.type == pygame.MOUSEBUTTONDOWN and self.__map.get_hero().get_ammo() > 0 \
                        and self.__map.get_reload_time() == 0:
                    """can choot with all mouse buttons"""
                    # self.__map.add_bullet()

                    """shoot only with left button"""
                    if event.button == 1:
                        self.__map.add_bullet()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        self.__map.set_reload_time(time())

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
            hero_alive = self.__map.check_collisions()
            """clears screen"""
            self.__screen.fill((0, 102, 0))
            """draws  map elements and ammo """
            self.draw_map(self.__map.get_camera_position())

            pygame.display.update()
            fps_clock.tick(fps)

        """Game Over manu"""
        click = False

        while game_over:
            self.__screen.fill((0, 0, 0))

            mx, my = pygame.mouse.get_pos()

            new_game = pygame.Rect(290, 400, 200, 50)
            if new_game.collidepoint((mx, my)):
                if click:
                    self.run()
                    break

            self.game_over_screen(new_game)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            fps_clock.tick(fps)

    def move_map_elements(self, move_direction_flags, fps):
        self.__map.move_hero(move_direction_flags, fps * 0.1)
        self.__map.move_monsters(fps * 0.02)
        self.__map.move_bullets()

    def draw_map(self, camera_position):

        """show grass"""
        self.__screen.blit(self.__map.get_grassland(), Vector2(0, 0),
                           pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))

        """show first aid kits"""
        for fsk in self.__map.get_firs_aid_kits():
            if self.__map.is_on_screen(fsk, self.__map.get_camera_position()):
                self.__screen.blit(fsk.get_image(), fsk.get_screen_position(self.__map.get_camera_position()))

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

        """shows forest on the screen"""
        self.__screen.blit(self.__map.get_borders(), Vector2(0, 0),
                           pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))

        """show map elements on the screen"""
        self.__screen.blit(self.__map.get_map_elements(), Vector2(0, 0),
                           pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))


        "draw hero health"
        pygame.draw.rect(self.__screen, (255, 0, 0), (20, 20, self.__map.get_hero().get_max_hp() * 35, 20))
        pygame.draw.rect(self.__screen, (0, 255, 0), (20, 20, self.__map.get_hero().get_hp() * 35, 20))

        "show remaining ammo"
        ammo_shift = 20
        for i in range(self.__map.get_hero().get_ammo()):
            self.__screen.blit(self.__map.get_bullet_image(), (ammo_shift, 520))
            ammo_shift += self.__map.get_bullet_image().get_size()[0]

        "show score"
        score = self.__font.render("Score " + str(self.__map.get_score()), True, (255, 255, 255))
        self.__screen.blit(score, (640, 10))

        "show reloading img"
        if self.__map.get_reload_time() != 0 and self.__map.get_reload_time() + 1 < time():
            self.__map.get_hero().set_ammo(8)
            self.__map.set_reload_time(0)
        elif self.__map.get_reload_time() != 0 and self.__map.get_reload_time() + 1 > time():
            self.__screen.blit(self.__map.get_rotated_image(), (370, 529))

    def set_map(self, map1):
        self.__map = map1

    def game_over_screen(self, button1):
        over = pygame.font.SysFont('arial', 80, bold=pygame.font.Font.bold).render("Game Over", True, (255, 255, 255))
        self.__screen.blit(over, (190, 100))
        score = pygame.font.SysFont('arial', 40).render("Your score " + str(self.__map.get_score()),
                                                        True, (255, 255, 255))
        self.__screen.blit(score, (300, 250))
        pygame.draw.rect(self.__screen, (255, 0, 0), button1)
        play = pygame.font.SysFont('arial', 30).render("Play Again", True, (255, 255, 255))
        self.__screen.blit(play, (330, 405))
