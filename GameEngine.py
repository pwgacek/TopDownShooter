from time import time

import pygame
from pygame.math import Vector2

from Map import Map


class GameEngine:
    def __init__(self):
        pygame.init()
        self.__width = 800
        self.__height = 600
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__map = Map(Vector2(self.__screen.get_size()))
        self.__font = pygame.font.SysFont('arial', 32, bold=pygame.font.Font.bold)
        self.__font2 = pygame.font.SysFont('arial', 44, bold=pygame.font.Font.bold)
        pygame.display.set_caption("Top-Down Shooter")

    def run(self):
        running = True
        hero_alive = True
        game_over = True
        grenade = False
        pistol = True
        shotgun = False
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

                if event.type == pygame.MOUSEBUTTONDOWN and self.__map.get_reload_time() == 0:
                    """can shoot with all mouse buttons"""
                    # self.__map.add_bullet()

                    if pistol and self.__map.get_hero().get_no_bullets_in_the_chamber() > 0:
                        """shoot only with left button"""
                        if event.button == 1:
                            self.__map.add_bullet()

                    elif grenade and self.__map.get_hero().get_no_grenades_in_pocket() > 0:
                        """shoot only with left button"""
                        if event.button == 1:
                            self.__map.add_grenade()

                    elif shotgun and self.__map.get_hero().get_no_shells_in_chamber() > 0:
                        """shoot only with left button"""
                        if event.button == 1:
                            self.__map.shotgun_shot()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if pistol:
                            pistol, grenade, shotgun = False, True, False
                        elif grenade:
                            pistol, grenade, shotgun = False, False, True
                        elif shotgun:
                            pistol, grenade, shotgun = True, False, False
                    elif event.button == 5:
                        if pistol:
                            pistol, grenade, shotgun = False, False, True
                        elif grenade:
                            pistol, grenade, shotgun = True, False, False
                        elif shotgun:
                            pistol, grenade, shotgun = False, True, False



                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        if pistol:
                            if self.__map.get_hero().get_no_ammo_packs() > 0:
                                self.__map.set_reload_time(time())
                        if grenade:
                            if self.__map.get_hero().get_no_grenades_packs() > 0:
                                self.__map.set_reload_time(time())

                        if shotgun:
                            if self.__map.get_hero().get_no_shotgun_packs() > 0:
                                self.__map.set_reload_time(time())

                    if event.key == pygame.K_3:
                        pistol = False
                        grenade = True
                        shotgun = False
                    elif event.key == pygame.K_2:
                        pistol = True
                        grenade = False
                        shotgun = False
                    elif event.key == pygame.K_1:
                        pistol = False
                        grenade = False
                        shotgun = True

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
            self.__map.check_collisions()
            hero_alive = self.__map.get_hero().get_hp() > 0
            """clears screen"""
            self.__screen.fill((0, 102, 0))
            """draws  map elements and ammo """
            self.draw_map(self.__map.get_camera_position(), pistol, grenade, shotgun)

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
        self.__map.move_bullets_and_grenades()

    def draw_map(self, camera_position, pistol, grenade, shotgun):

        """show grass"""
        self.__screen.blit(self.__map.get_grassland(), Vector2(0, 0),
                           pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))

        """show dropped items"""
        for item in self.__map.get_dropped_items():
            if self.__map.is_on_screen(item, self.__map.get_camera_position()):
                self.__screen.blit(item.get_image(), item.get_screen_position(self.__map.get_camera_position()))

        """shows hero on the screen"""
        self.__screen.blit(self.__map.get_hero().get_rotated_image(), self.__map.get_hero().get_screen_position())

        """shows monsters on the screen"""
        for monster in self.__map.get_monsters():
            if self.__map.is_on_screen(monster, self.__map.get_camera_position()):
                self.__screen.blit(monster.get_rotated_image(),
                                   monster.get_screen_position(self.__map.get_camera_position()))

        """shows bullets and grenades, their movement and removal"""

        for bullet in self.__map.get_bullets():
            if self.__map.is_on_screen(bullet, self.__map.get_camera_position()):
                self.__screen.blit(pygame.transform.rotate(pygame.image.load("assets/bullet.png"),
                                                           bullet.get_angle() - 90),
                                   bullet.get_screen_position(self.__map.get_camera_position()))

        for grenadee in self.__map.get_grenades():
            if self.__map.is_on_screen(grenadee, self.__map.get_camera_position()):
                self.__screen.blit(pygame.transform.rotate(pygame.image.load("assets/grenade.png"),
                                                           grenadee.get_angle() - 90),
                                   grenadee.get_screen_position(self.__map.get_camera_position()))

        """shows forest on the screen"""
        self.__screen.blit(self.__map.get_borders(), Vector2(0, 0),
                           pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))

        """show map elements on the screen"""
        self.__screen.blit(self.__map.get_map_elements(), Vector2(0, 0),
                           pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))

        "draw hero health"
        pygame.draw.rect(self.__screen, (255, 0, 0), (20, 20, self.__map.get_hero().get_max_hp() * 35, 20))
        pygame.draw.rect(self.__screen, (0, 255, 0), (20, 20, self.__map.get_hero().get_hp() * 35, 20))

        "show remaining ammo in chamber"
        ammo_shift = 20
        if pistol:
            for i in range(self.__map.get_hero().get_no_bullets_in_the_chamber()):
                self.__screen.blit(self.__map.get_bullet_image(), (ammo_shift, 520))
                ammo_shift += self.__map.get_bullet_image().get_size()[0]
        elif grenade:
            for i in range(self.__map.get_hero().get_no_grenades_in_pocket()):
                self.__screen.blit(self.__map.get_grenade_image(), (ammo_shift, 520))
                ammo_shift += self.__map.get_grenade_image().get_size()[0]
        elif shotgun:
            for i in range(self.__map.get_hero().get_no_shells_in_chamber()):
                self.__screen.blit(self.__map.get_shell_image(), (ammo_shift, 500))
                ammo_shift += self.__map.get_shell_image().get_size()[0]

        "show score"
        score = self.__font.render("Score " + str(self.__map.get_score()), True, (255, 255, 255))
        self.__screen.blit(score, (640, 10))
        "show remaining ammo"
        x = ""
        if pistol:
            x = "p"
            self.__screen.blit(self.__map.get_ammo_image(), (660, 510))
        elif grenade:
            x = "g"
            self.__screen.blit(self.__map.get_grenades_image(), (600, 510))
        elif shotgun:
            x = "s"
            self.__screen.blit(self.__map.get_shotgun_shells_image(), (640, 510))

        ammo = self.__font2.render(str(self.__map.get_hero().get_no_ammo(x)), True, (255, 255, 255))
        self.__screen.blit(ammo, (715, 530))

        "show reloading img"
        if self.__map.get_reload_time() != 0 and self.__map.get_reload_time() + 1 < time():
            no_ammo_packs = self.__map.get_hero().get_no_ammo_packs()
            no_grenades = self.__map.get_hero().get_no_grenades_packs()
            no_shotgun = self.__map.get_hero().get_no_shotgun_packs()
            if no_ammo_packs > 0 and pistol:
                self.__map.get_hero().change_no_ammo_packs(-1)
                self.__map.get_hero().set_no_bullets_in_the_chamber(8)
                self.__map.set_reload_time(0)

            if no_grenades > 0 and grenade:
                self.__map.get_hero().change_no_grenades_packs(-1)
                self.__map.get_hero().set_no_grenades_in_pocket(3)
                self.__map.set_reload_time(0)

            if no_shotgun > 0 and shotgun:
                self.__map.get_hero().change_no_shotgun_packs(-1)
                self.__map.get_hero().set_no_shells_in_chamber(4)
                self.__map.set_reload_time(0)

        elif self.__map.get_reload_time() != 0 and self.__map.get_reload_time() + 1 > time():
            self.__screen.blit(self.__map.get_rotated_reload_image(), (370, 529))

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
