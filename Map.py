import math
from random import randint
from time import time

import pygame
from pygame.math import Vector2

from Bullet import Bullet
from Hero import Hero
from MapGenerator import generate_array, generate_borders, generate_grass, generate_map_elements
from Monster import Monster
from FirstAidKit import FirstAidKit


class Map:
    def __init__(self, screen_size):
        self.__size = Vector2(4800, 4800)
        self.__chunk_size = 50
        self.__screen_size = screen_size
        self.__array = generate_array(30, self.__size.y, self.__size.y, self.__chunk_size, self.__screen_size)
        self.__hero = Hero(Vector2(self.__size.x / 2, self.__size.y / 2), self.__screen_size)
        self.__bullets = list()
        # self.__font = pygame.font.SysFont('Bradley Hand ITC', 50, bold=pygame.font.Font.bold)
        self.__monsters = list()
        self.__first_aid_kits = list()
        self.__bullet_image = pygame.image.load("assets/ammo1.png")
        self.__reload = pygame.image.load("assets/reload.png")
        self.__reload_angle = 0
        self.__reload_time = 0
        self.__borders = generate_borders(self.__chunk_size,
                                          Vector2(self.__size.x, self.__size.y), self.__array)
        self.__grassland = generate_grass(self.__chunk_size,
                                          Vector2(self.__size.x, self.__size.y), self.__array)
        self.__map_elements = generate_map_elements(self.__chunk_size,
                                                    Vector2(self.__size.x, self.__size.y), self.__array)
        self.__min_no_monsters = 5
        self.__score = 0

    def move_hero(self, move_direction_flags, move_speed):
        if (move_direction_flags["down"] and move_direction_flags["up"]) or \
                not (move_direction_flags["down"] or move_direction_flags["up"]):
            change_y = 0
        elif move_direction_flags["down"]:
            change_y = move_speed
        else:
            change_y = -move_speed

        if (move_direction_flags["left"] and move_direction_flags["right"]) or \
                not (move_direction_flags["left"] or move_direction_flags["right"]):
            change_x = 0
        elif move_direction_flags["left"]:
            change_x = -move_speed
        else:
            change_x = move_speed

        current_x = self.__hero.get_map_position().x + self.__hero.get_image().get_size()[0] / 2
        current_y = self.__hero.get_map_position().y + self.__hero.get_image().get_size()[1] / 2
        destination_x = current_x + change_x
        destination_y = current_y + change_y

        """maintain speed when moving diagonally"""
        if change_x and change_y and self.__hero_can_move_to(Vector2(destination_x, destination_y)):
            change_x /= math.sqrt(2)
            change_y /= math.sqrt(2)

        """change position if possible"""
        if self.__hero_can_move_to(Vector2(destination_x, current_y)):
            self.__hero.get_map_position().x += change_x
        if self.__hero_can_move_to(Vector2(current_x, destination_y)):
            self.__hero.get_map_position().y += change_y

        self.__hero.set_angle()

    def move_monsters(self, move_speed):
        faster = move_speed
        slower = move_speed * 0.3
        monster_freeze_time = 1
        max_distance = self.__hero.get_image().get_size()[1] / 2

        for monster in self.__monsters:
            if math.dist(monster.get_map_position(), self.__hero.get_map_position()) > max_distance:

                """monster moves slower after being hit"""
                if monster.get_time() != 0:
                    if monster.get_time() + monster_freeze_time > time():
                        move_speed = slower
                    else:
                        monster.set_time()
                else:
                    move_speed = faster

                shift = Monster.get_image().get_size()[0] / 2

                angles = [0, 30, -30, 60, -60, 87, -87]
                """checks if monster can move in given direction"""
                for a in angles:
                    vector = monster.get_unit_vector(monster.get_angle() + a)
                    x = monster.get_map_position().x + shift + vector.x * move_speed
                    y = monster.get_map_position().y + shift + vector.y * move_speed

                    can_move = True

                    for other_monster in self.__monsters:
                        distance = math.dist(monster.get_map_position(), other_monster.get_map_position())

                        if not self.__no_obstacles_for_monster(Vector2(x, y)):
                            can_move = False
                        elif other_monster != monster and distance < max_distance:
                            """Given monster can't go straight check if he turn left or right """

                            if distance >= math.dist(Vector2(x - shift, y - shift), other_monster.get_map_position()):
                                can_move = False
                                break

                    if can_move:
                        monster.get_map_position().x = x - shift
                        monster.get_map_position().y = y - shift
                        break

                monster.set_angle(self.__hero.get_map_position())

    def get_camera_position(self):
        """get position of rectangle (cut out of background image) which will be shown on the screen"""
        camera_x = self.__hero.get_map_position().x - self.__hero.get_screen_position().x
        camera_y = self.__hero.get_map_position().y - self.__hero.get_screen_position().y
        return Vector2(camera_x, camera_y)

    def __hero_can_move_to(self, v):
        cords = self.__get_cords_in_array(v)
        shift = Monster.get_image().get_width() // 2

        for monster in self.__monsters:
            v2 = Vector2(monster.get_map_position().x + shift, monster.get_map_position().y + shift)

            if math.dist(v, v2) < self.__hero.get_image().get_size()[1] / 2:
                return False
        return self.__array[int(cords.x)][int(cords.y)] % 2

    def __no_obstacles_for_monster(self, v):
        cords = self.__get_cords_in_array(v)
        return self.__array[int(cords.x)][int(cords.y)] != 2

    def __bullet_hit_map_element(self, v):
        cords = self.__get_cords_in_array(v)
        return self.__array[int(cords.x)][int(cords.y)] % 2 == 0

    def get_hero(self):
        return self.__hero

    def add_bullet(self):
        self.__hero.set_ammo(self.__hero.get_ammo() - 1)
        a = self.__hero.get_map_position().x
        b = self.__hero.get_map_position().y

        map_position = Vector2(a, b)
        angle = self.__hero.get_angle() + 90

        hero_size = self.__hero.get_image().get_size()
        self.__bullets.append(Bullet(map_position, angle, hero_size))

    def move_bullets(self):
        for bullet in self.__bullets:
            bullet.move()

        self.remove_bullets()

    def remove_bullets(self):
        for i in self.__bullets:
            if self.bullet_not_in_bounds(i) or self.__bullet_hit_map_element(i.get_map_position()):
                self.__bullets.remove(i)

    def bullet_not_in_bounds(self, bullet):
        return bullet.get_map_position()[0] > self.__size.x or bullet.get_map_position()[1] > self.__size.y or \
               bullet.get_map_position()[0] < 0 or bullet.get_map_position()[1] < 0

    def get_monsters(self):
        return self.__monsters

    def get_bullets(self):
        return self.__bullets

    def get_firs_aid_kits(self):
        return self.__first_aid_kits

    # def get_font(self):
    #     return self.__font

    # screen.blit(self.__font.render("Reload (r)", True, (255, 0, 0)), (400, 530))

    def add_monster(self):
        """randomly places monster on the edge of map"""
        if randint(0, 1):
            if randint(0, 1):
                x = 2 * self.__chunk_size
            else:
                x = self.__size.x - 2 * self.__chunk_size

            y = randint(2 * self.__chunk_size, int(self.__size.y - 2 * self.__chunk_size))

        else:
            if randint(0, 1):
                y = 2 * self.__chunk_size
            else:
                y = self.__size.y - 2 * self.__chunk_size

            x = randint(2 * self.__chunk_size, int(self.__size.x) - 2 * self.__chunk_size)

        self.__monsters.append(Monster(Vector2(x, y)))

    def __remove_monster(self, monster):
        self.__monsters.remove(monster)

    def is_on_screen(self, sth, camera_position):
        return 0 < sth.get_screen_position(camera_position).x + sth.get_image().get_size()[0] \
               and sth.get_screen_position(camera_position).x < self.__screen_size.x \
               and 0 < sth.get_screen_position(camera_position).y + sth.get_image().get_size()[1] \
               and sth.get_screen_position(camera_position).y < self.__screen_size.y

    def __get_cords_in_array(self, v):
        return Vector2(v.x // self.__chunk_size, v.y // self.__chunk_size)

    def get_chunk_size(self):
        return self.__chunk_size

    def get_borders(self):
        return self.__borders

    def get_grassland(self):
        return self.__grassland

    def get_map_elements(self):
        return self.__map_elements

    def get_bullet_image(self):
        return self.__bullet_image

    def keep_no_monsters(self):
        no_needed_monsters = self.__min_no_monsters - len(self.__monsters)
        if no_needed_monsters > 0:
            for i in range(no_needed_monsters):
                self.add_monster()

    def increase_min_no_monsters(self, num):
        self.__min_no_monsters += num

    def score_point(self):
        self.__score += 1

    def get_score(self):
        return self.__score

    def get_distance(self, obj1, obj2):
        x1, y1 = obj1.get_map_position()
        x1 += obj1.get_image().get_width() / 2
        y1 += obj1.get_image().get_height() / 2

        x2, y2 = obj2.get_map_position()
        x2 += obj2.get_image().get_width() / 2
        y2 += obj2.get_image().get_height() / 2

        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def check_collisions(self):
        bullet_h = Bullet.get_image().get_height() * 2 / 5
        monster_h = Monster.get_image().get_height() * 2 / 5
        hero_h = self.__hero.get_image().get_height() * 2 / 5

        """hero takes first aid kit"""
        for fak in self.__first_aid_kits:
            if self.get_distance(self.__hero, fak) < self.__hero.get_image().get_width() // 2:
                self.__hero.heal()
                self.__first_aid_kits.remove(fak)

        """bullet hits monster"""
        for bullet in self.__bullets:
            for monster in self.__monsters:
                if self.get_distance(monster, bullet) < bullet_h + monster_h:
                    self.__bullets.remove(bullet)
                    monster.hurt(time())

                    if monster.get_hp() == 0:
                        if randint(0, 10) == 10:
                            """drops first aid kit"""
                            shift = monster.get_image().get_size()[0] // 2
                            pos = Vector2(monster.get_map_position().x + shift, monster.get_map_position().y + shift)
                            self.__first_aid_kits.append(FirstAidKit(pos))
                        self.__monsters.remove(monster)
                        self.score_point()
                    break

        """monster attacks hero"""
        for monster in self.__monsters:
            if self.get_distance(self.__hero, monster) < monster_h + hero_h:
                if monster.get_last_attack() == 0 or monster.get_last_attack() + 1 < time():
                    monster.attack()
                    self.__hero.hurt()

    def get_reload_icon(self):
        return self.__reload

    def set_score(self, score):
        self.__score = score

    def get_rotated_image(self):
        """ returns rotated  image while keeping its center and size"""

        orig_rect = self.__reload.get_rect()
        rot_image = pygame.transform.rotate(self.__reload, self.__reload_angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.__reload_angle += -5
        return rot_image

    def get_reload_time(self):
        return self.__reload_time

    def set_reload_time(self, time1):
        self.__reload_time = time1
