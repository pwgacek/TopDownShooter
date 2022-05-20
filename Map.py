import math
from random import randint
from time import time

import pygame
from pygame.math import Vector2

from Bullet import Bullet
from Hero import Hero
from MapGenerator import generate_array, generate_borders, generate_grass, generate_map_elements
from Monster import Monster
from Grenade import Grenade


def get_distance(obj1, obj2):
    x1, y1 = obj1.get_map_position()
    x1 += obj1.get_image().get_width() / 2
    y1 += obj1.get_image().get_height() / 2

    x2, y2 = obj2.get_map_position()
    x2 += obj2.get_image().get_width() / 2
    y2 += obj2.get_image().get_height() / 2

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Map:
    def __init__(self, screen_size):
        self.__size = Vector2(4800, 4800)
        self.__chunk_size = 50
        self.__screen_size = screen_size
        self.__array = generate_array(30, self.__size.y, self.__size.y, self.__chunk_size, self.__screen_size)
        self.__hero = Hero(Vector2(self.__size.x / 2, self.__size.y / 2), self.__screen_size)
        self.__bullets = list()
        self.__grenades = list()
        # self.__font = pygame.font.SysFont('Bradley Hand ITC', 50, bold=pygame.font.Font.bold)
        self.__monsters = list()
        self.__dropped_items = list()

        self.__bullet_image = pygame.image.load("assets/ammo1.png")
        self.__grenade_image = pygame.image.load("assets/grenade_ico.png")
        self.__shell_image = pygame.image.load("assets/shotgun_shell.png")
        self.__reload_image = pygame.image.load("assets/reload.png")
        self.__ammo_image = pygame.image.load("assets/ammo_pack2.png")
        self.__grenades_image = pygame.image.load("assets/many_granedesv2.png")
        self.__shotgun_shells_image = pygame.image.load("assets/shotgun_shellsv2.png")
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

        current_x = self.__hero.get_map_position().x + self.__hero.get_size().x / 2
        current_y = self.__hero.get_map_position().y + self.__hero.get_size().y / 2
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
        max_distance = self.__hero.get_size().x / 2
        shift = Monster.get_size().x / 2
        near_monsters_pos = list()
        for monster in self.__monsters:
            if get_distance(monster, self.__hero) > max_distance:

                """monster moves slower after being hit"""
                if monster.get_time() != 0:
                    if monster.get_time() + monster_freeze_time > time():
                        move_speed = slower
                    else:
                        monster.set_time()
                else:
                    move_speed = faster

                monster_x = monster.get_map_position().x + shift
                monster_y = monster.get_map_position().y + shift

                near_monsters_pos.clear()
                for other_monster in self.__monsters:
                    if monster is not other_monster and get_distance(monster, other_monster) < max_distance:
                        near_monsters_pos.append(other_monster.get_map_position())

                """checks if monster can move in given direction"""
                for a in [0, 30, -30, 60, -60, 87, -87]:
                    vector = monster.get_unit_vector(monster.get_angle() + a)
                    x = monster_x + vector.x * move_speed * monster.get_speed_ratio()
                    y = monster_y + vector.y * move_speed * monster.get_speed_ratio()

                    can_move = True
                    if not self.__no_obstacles_for_monster(Vector2(x, y)):
                        can_move = False
                    else:
                        for other_monster_pos in near_monsters_pos:

                            if math.dist(monster.get_map_position(), other_monster_pos) \
                                    >= math.dist(Vector2(x - shift, y - shift), other_monster_pos):
                                can_move = False
                                break

                    if can_move:
                        monster.get_map_position().x = x - shift
                        monster.get_map_position().y = y - shift
                        break

                monster.set_angle(self.__hero)

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

            if math.dist(v, v2) < self.__hero.get_size().x / 2:
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
        self.__hero.set_no_bullets_in_the_chamber(self.__hero.get_no_bullets_in_the_chamber() - 1)

        a = self.__hero.get_map_position().x
        b = self.__hero.get_map_position().y

        map_position = Vector2(a, b)
        angle = self.__hero.get_angle() + 90

        self.__bullets.append(Bullet(map_position, angle, self.__hero.get_size()))

    def shotgun_shot(self):
        self.__hero.set_no_shells_in_chamber(self.__hero.get_no_shells_in_chamber() - 1)

        a = self.__hero.get_map_position().x
        b = self.__hero.get_map_position().y

        map_position = Vector2(a, b)
        angle = self.__hero.get_angle() + 90

        for i in range(4):
            self.__bullets.append(Bullet(map_position, angle-15 + i*10, self.__hero.get_size()))

    def add_grenade(self):
        self.__hero.set_no_grenades_in_pocket(self.__hero.get_no_grenades_in_pocket() - 1)

        a = self.__hero.get_map_position().x
        b = self.__hero.get_map_position().y

        map_position = Vector2(a, b)
        angle = self.__hero.get_angle() + 90

        self.__grenades.append(Grenade(map_position, angle, self.__hero.get_size()))

    def move_bullets_and_grenades(self, move_speed):
        for bullet in self.__bullets:
            bullet.move(move_speed)

        for grenade in self.__grenades:
            grenade.move(move_speed / 2)

        self.remove_bullets_and_grenades()

    def remove_bullets_and_grenades(self):
        for i in self.__bullets:
            if self.bullet_not_in_bounds(i) or self.__bullet_hit_map_element(i.get_map_position()):
                self.__bullets.remove(i)

        for i in self.__grenades:
            if self.bullet_not_in_bounds(i) or self.__bullet_hit_map_element(i.get_map_position()):
                self.grenade_explode(i)

    def bullet_not_in_bounds(self, bullet):
        return bullet.get_map_position()[0] > self.__size.x or bullet.get_map_position()[1] > self.__size.y or \
               bullet.get_map_position()[0] < 0 or bullet.get_map_position()[1] < 0

    def get_monsters(self):
        return self.__monsters

    def get_bullets(self):
        return self.__bullets

    def get_grenades(self):
        return self.__grenades

    def get_dropped_items(self):
        return self.__dropped_items

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
        return 0 < sth.get_screen_position(camera_position).x + sth.get_size().x \
               and sth.get_screen_position(camera_position).x < self.__screen_size.x \
               and 0 < sth.get_screen_position(camera_position).y + sth.get_size().x \
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

    def get_ammo_image(self):
        return self.__ammo_image

    def get_grenade_image(self):
        return self.__grenade_image

    def get_grenades_image(self):
        return self.__grenades_image

    def get_shell_image(self):
        return self.__shell_image

    def get_shotgun_shells_image(self):
        return self.__shotgun_shells_image

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

    def check_collisions(self):
        bullet_h = Bullet.get_image().get_height() * 2 / 5
        monster_h = Monster.get_image().get_height() * 2 / 5
        hero_h = self.__hero.get_image().get_height() * 2 / 5

        """hero grabs dropped item"""
        dist = self.__hero.get_image().get_width() // 2
        for item in self.__dropped_items:
            if get_distance(self.__hero, item) < dist:
                self.__hero.pick_up_dropped_item(item)
                self.__dropped_items.remove(item)

        """bullet hits monster"""
        for bullet in self.__bullets:
            for monster in self.__monsters:
                if self.monster_bullet_collision(monster, bullet, "b"):
                    break

        """grenades explode (time)"""
        now = time()
        grenade_time_to_explode = 2
        for grenade in self.__grenades:
            if now - grenade.get_time() >= grenade_time_to_explode:
                self.grenade_explode(grenade)

        """grenades hit monster"""
        for grenade in self.__grenades:
            for monster in self.__monsters:
                if self.monster_bullet_collision(monster, grenade, "g"):
                    break

        """monster attacks hero"""
        for monster in self.__monsters:
            if get_distance(self.__hero, monster) < monster_h + hero_h:
                if monster.get_last_attack() == 0 or monster.get_last_attack() + 1 < time():

                    monster.attack()
                    self.__hero.hurt()
                    
        for bullet in self.__bullets:
            if get_distance(self.__hero, bullet) < bullet_h + hero_h:
                self.__bullets.remove(bullet)
                self.__hero.hurt()

    def monster_bullet_collision(self, monster, bullet, weapon_type):
        bullet_h = Bullet.get_image().get_height() * 2 / 5
        monster_h = Monster.get_image().get_height() * 2 / 5
        grenade_h = Grenade.get_image().get_height() * 2 / 5
        if weapon_type == "b":
            h = bullet_h
        elif weapon_type == "g":
            h = grenade_h
        if get_distance(monster, bullet) < h + monster_h:
            if weapon_type == "b":
                self.__bullets.remove(bullet)
            elif weapon_type == "g":
                self.grenade_explode(bullet)

            monster.hurt(time())

            if monster.get_hp() == 0:
                dropped_item = monster.drop_item()
                if dropped_item is not None:
                    self.__dropped_items.append(dropped_item)

                self.__monsters.remove(monster)
                self.score_point()
            return True
        return False

    def grenade_explode(self, grenade):
        pos = grenade.get_map_position()
        ang = grenade.get_angle()
        self.__grenades.remove(grenade)

        for i in range(16):
            self.__bullets.append(Bullet(pos, ang + (i+1)*22.5, Vector2(0,0)))

    def get_reload_image(self):
        return self.__reload_image

    def set_score(self, score):
        self.__score = score

    def get_rotated_reload_image(self):
        """ returns rotated  image while keeping its center and size"""

        orig_rect = self.__reload_image.get_rect()
        rot_image = pygame.transform.rotate(self.__reload_image, self.__reload_angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.__reload_angle += -5
        return rot_image

    def get_reload_time(self):
        return self.__reload_time

    def set_reload_time(self, time1):
        self.__reload_time = time1
