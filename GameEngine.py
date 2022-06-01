from time import time

import pygame
from pygame.math import Vector2

from Map import Map
from ImageHandler import ImageHandler
from Weapon import WeaponType


class GameEngine:
    def __init__(self):
        pygame.init()
        self.__width = 800
        self.__height = 600
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__map = Map(Vector2(self.__screen.get_size()))
        self.__image_handler = ImageHandler(self.__map.chunk_size, self.__map.size, self.__map.array)
        self.__font = pygame.font.SysFont('arial', 32, bold=pygame.font.Font.bold)
        self.__font2 = pygame.font.SysFont('arial', 44, bold=pygame.font.Font.bold)
        self.__dt = 0.1

        pygame.display.set_caption("Top-Down Shooter")

    def run(self):
        running = True
        hero_alive = True
        game_over = True
        fps = 60
        fps_clock = pygame.time.Clock()
        monster_clock = pygame.time.Clock()
        self.__map = Map(Vector2(self.__screen.get_size()))
        self.__image_handler = ImageHandler(self.__map.chunk_size, self.__map.size, self.__map.array)
        delta = 0
        """set true if key is pressed"""
        move_direction_flags = {"up": False, "down": False, "left": False, "right": False}

        last_time = time() - 0.1

        """main game loop"""
        while running and hero_alive:
            self.__dt = time() - last_time
            last_time = time()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    game_over = False

                if event.type == pygame.MOUSEBUTTONDOWN and self.__image_handler.reload_time == 0:
                    """can shoot with all mouse buttons"""
                    # self.__map.add_bullet()

                    """shoot only with left button"""
                    if event.button == 1:
                        curr_weapon = self.__map.hero.weapons.current_weapon
                        in_chamber = self.__map.hero.weapons.in_chamber
                        if curr_weapon == WeaponType.pistol and in_chamber > 0:
                            self.__map.add_bullet(1)

                        elif curr_weapon == WeaponType.grenade and in_chamber > 0:
                            self.__map.add_grenade()

                        elif curr_weapon == WeaponType.shotgun and in_chamber > 0:
                            self.__map.shotgun_shot(1)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.__map.hero.weapons.set_next_weapon()
                    elif event.button == 5:
                        self.__map.hero.weapons.set_prev_weapon()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if self.__map.hero.weapons.packs > 0:
                            self.__image_handler.reload_time = (time())

                    if event.key == pygame.K_3:
                        self.__map.hero.weapons.update_current_weapon(WeaponType.grenade)
                    elif event.key == pygame.K_2:
                        self.__map.hero.weapons.update_current_weapon(WeaponType.pistol)
                    elif event.key == pygame.K_1:
                        self.__map.hero.weapons.update_current_weapon(WeaponType.shotgun)

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
            if delta > len(self.__map.monsters) * 800:
                self.__map.increase_min_no_monsters(1)
                delta = 0
            """move all map elements"""
            self.__move_map_elements(move_direction_flags)
            self.__map.check_collisions()
            hero_alive = self.__map.hero.hp > 0
            """clears screen"""
            self.__screen.fill((0, 102, 0))
            """draws  map elements and ammo """
            self.__draw_all(self.__map.camera_position)

            pygame.display.update()
            fps_clock.tick(int(fps / (1 + len(self.__map.monsters) * 0.01)))

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

    def __move_map_elements(self, move_direction_flags):
        self.__map.move_hero(move_direction_flags, self.__dt * 300)
        self.__map.move_monsters(self.__dt * 75)
        self.__map.move_bullets_and_grenades(self.__dt * 1000)

    def __draw_all(self, camera_position):

        """show grass"""
        self.__screen.blit(self.__image_handler.grassland_image, Vector2(0, 0),
                           pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))

        """show dropped items"""
        for item in self.__map.dropped_items:
            if self.__map.is_on_screen(item):
                self.__screen.blit(item.image, self.__map.get_screen_position(item))

        """shows hero on the screen"""
        self.__screen.blit(self.__map.hero.rotated_image, self.__map.hero.screen_position)

        """shows monsters on the screen"""
        for monster in self.__map.monsters:
            if self.__map.is_on_screen(monster):
                self.__screen.blit(monster.rotated_image, self.__map.get_screen_position(monster))

        """shows bullets and grenades, their movement and removal"""

        for bullet in self.__map.bullets:
            if self.__map.is_on_screen(bullet):
                self.__screen.blit(pygame.transform.rotate(pygame.image.load("assets/bullet.png"), bullet.angle - 90),
                                   self.__map.get_screen_position(bullet))

        for grenade in self.__map.grenades:
            if self.__map.is_on_screen(grenade):
                self.__screen.blit(pygame.transform.rotate(pygame.image.load("assets/grenade.png"), grenade.angle - 90),
                                   self.__map.get_screen_position(grenade))

        """shows forest on the screen"""
        self.__screen.blit(self.__image_handler.borders_image, Vector2(0, 0),
                           pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))

        """show map elements on the screen"""
        self.__screen.blit(self.__image_handler.map_elements_image, Vector2(0, 0),
                           pygame.Rect(camera_position.x, camera_position.y, self.__width, self.__height))

        "draw hero health"
        pygame.draw.rect(self.__screen, (255, 0, 0), (20, 20, self.__map.hero.max_hp * 35, 20))
        pygame.draw.rect(self.__screen, (0, 255, 0), (20, 20, self.__map.hero.hp * 35, 20))

        "show score"
        score = self.__font.render("Score " + str(self.__map.score), True, (255, 255, 255))
        self.__screen.blit(score, (640, 10))

        """show fps"""
        curren_fps = self.__font.render("fps:" + str(int(1.0 // self.__dt)), True, (255, 255, 255))
        self.__screen.blit(curren_fps, (500, 10))

        """show no_monsters"""
        no_monsters = self.__font.render("m:" + str(len(self.__map.monsters)), True, (255, 255, 255))
        self.__screen.blit(no_monsters, (400, 10))

        "show remaining ammo and draw ammo in chamber"
        ammo_shift = 20
        pos = (ammo_shift, 520)
        img = None
        curr_weapon = self.__map.hero.weapons.current_weapon

        if curr_weapon == WeaponType.pistol:
            img = self.__image_handler.bullet_image
            self.__screen.blit(self.__image_handler.ammo_image, (660, 510))
        elif curr_weapon == WeaponType.grenade:
            img = self.__image_handler.grenade_image
            self.__screen.blit(self.__image_handler.grenades_image, (600, 510))
        elif curr_weapon == WeaponType.shotgun:
            img = self.__image_handler.shell_image
            pos = (pos[0], 500)
            self.__screen.blit(self.__image_handler.shotgun_shells_image, (640, 510))

        img_size = img.get_size()[0]

        for i in range(self.__map.hero.weapons.in_chamber):
            self.__screen.blit(img, pos)
            ammo_shift += img_size
            pos = (ammo_shift, pos[1])

        ammo = self.__font2.render(str(self.__map.hero.get_no_ammo()), True, (255, 255, 255))
        self.__screen.blit(ammo, (715, 530))

        "show reloading img"
        if self.__image_handler.reload_time != 0 and self.__image_handler.reload_time + 1 < time():
            ammo_packs = self.__map.hero.weapons.packs
            if ammo_packs > 0:
                self.__map.hero.weapons.updated_ammo_packs(curr_weapon, -1)
                self.__map.hero.weapons.reload()
                self.__image_handler.reload_time = 0

        elif self.__image_handler.reload_time != 0 and self.__image_handler.reload_time + 1 > time():
            self.__screen.blit(self.__image_handler.rotated_reload_image, (370, 529))

    def game_over_screen(self, button1):
        over = pygame.font.SysFont('arial', 80, bold=pygame.font.Font.bold).render("Game Over", True, (255, 255, 255))
        self.__screen.blit(over, (190, 100))
        score = pygame.font.SysFont('arial', 40).render("Your score " + str(self.__map.score),
                                                        True, (255, 255, 255))
        self.__screen.blit(score, (300, 250))
        pygame.draw.rect(self.__screen, (255, 0, 0), button1)
        play = pygame.font.SysFont('arial', 30).render("Play Again", True, (255, 255, 255))
        self.__screen.blit(play, (330, 405))
