import math
from random import randint
from time import time

from pygame.math import Vector2

from Bullet import Bullet
from Hero import Hero
from MapGenerator import generate_array
from Monster import Monster
from Grenade import Grenade
from Utils import get_distance, center_map_position


class Map:
    def __init__(self, screen_size):
        self.__size = Vector2(4800, 4800)
        self.__chunk_size = 50
        self.__screen_size = screen_size
        self.__array = generate_array(30, self.__size.x, self.__size.y, self.__chunk_size, self.__screen_size)
        self.__hero = Hero(Vector2(self.__size.x / 2, self.__size.y / 2), self.__screen_size)

        self.__bullets = list()
        self.__grenades = list()
        self.__monsters = list()
        self.__dropped_items = list()

        self.__min_no_monsters = 15
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

        current_x, current_y = center_map_position(self.__hero)

        destination_x = current_x + change_x
        destination_y = current_y + change_y

        """maintain speed when moving diagonally"""
        if change_x and change_y and self.__hero_can_move_to(Vector2(destination_x, destination_y)):
            change_x /= math.sqrt(2)
            change_y /= math.sqrt(2)

        """change position if possible"""
        if self.__hero_can_move_to(Vector2(destination_x, current_y)):
            self.__hero.map_position.x += change_x
            current_x = destination_x
        if self.__hero_can_move_to(Vector2(current_x, destination_y)):
            self.__hero.map_position.y += change_y

        self.__hero.update_angle()

    def move_monsters(self, move_speed):
        monster_freeze_time = 1
        max_distance = self.__hero.size.x / 2
        shift = Monster.size.x / 2
        near_monsters_pos = list()
        for monster in self.__monsters:
            monster_move_speed = move_speed
            if get_distance(monster, self.__hero) > max_distance:

                """monster moves slower after being hit"""
                if monster.shot_time != 0:
                    if monster.shot_time + monster_freeze_time > time():
                        monster_move_speed = move_speed * 0.3
                    else:
                        monster.reset_shot_time()

                near_monsters_pos.clear()
                for other_monster in self.__monsters:
                    if monster is not other_monster and get_distance(monster, other_monster) < max_distance:
                        near_monsters_pos.append(other_monster.map_position)

                """checks if monster can move in given direction"""
                for a in [0, 30, -30, 60, -60, 87, -87]:
                    vector = monster.get_unit_vector(monster.angle + a)
                    x = monster.map_position.x + vector.x * monster_move_speed * monster.speed_ratio
                    y = monster.map_position.y + vector.y * monster_move_speed * monster.speed_ratio

                    can_move = True
                    if not self.__no_obstacles_for_monster(Vector2(x + shift, y + shift)):
                        can_move = False
                    else:
                        for other_monster_pos in near_monsters_pos:

                            if math.dist(monster.map_position, other_monster_pos) \
                                    >= math.dist(Vector2(x, y), other_monster_pos):
                                can_move = False
                                break

                    if can_move:
                        monster.map_position.x = x
                        monster.map_position.y = y
                        break

                monster.update_angle(self.__hero)

    def move_bullets_and_grenades(self, move_speed):
        for bullet in self.__bullets:
            bullet.move(move_speed)

        for grenade in self.__grenades:
            grenade.move(move_speed / 2)

        self.__remove_bullets_and_grenades()

    def __hero_can_move_to(self, v):
        cords = self.__get_cords_in_array(v)

        for monster in self.__monsters:

            if math.dist(v, center_map_position(monster)) < self.__hero.size.x / 2:
                return False
        return self.__array[int(cords.x)][int(cords.y)] % 2

    def __no_obstacles_for_monster(self, v):
        cords = self.__get_cords_in_array(v)
        return self.__array[int(cords.x)][int(cords.y)] != 2

    def __bullet_hit_map_element(self, v):
        cords = self.__get_cords_in_array(v)
        return self.__array[int(cords.x)][int(cords.y)] % 2 == 0

    def add_bullet(self, damage):
        self.__hero.set_no_bullets_in_the_chamber(self.__hero.get_no_bullets_in_the_chamber() - 1)
        angle = self.__hero.angle + 90
        self.__bullets.append(Bullet(center_map_position(self.__hero), angle, damage))

    def add_grenade(self):
        self.__hero.set_no_grenades_in_pocket(self.__hero.get_no_grenades_in_pocket() - 1)
        angle = self.__hero.angle + 90
        self.__grenades.append(Grenade(center_map_position(self.__hero), angle, time()))

    def shotgun_shot(self, damage):
        self.__hero.set_no_shells_in_chamber(self.__hero.get_no_shells_in_chamber() - 1)

        angle = self.__hero.angle + 90

        for i in range(4):
            self.__bullets.append(Bullet(center_map_position(self.__hero), angle - 15 + i * 10, damage))

    def __remove_bullets_and_grenades(self):
        for i in self.__bullets:
            if self.__bullet_not_in_bounds(i):
                self.__bullets.remove(i)

        for i in self.__grenades:
            if self.__bullet_not_in_bounds(i):
                self.__grenades.remove(i)

    def __bullet_not_in_bounds(self, bullet):
        return bullet.map_position.x > self.__size.x or bullet.map_position.y > self.__size.y or \
               bullet.map_position.x < 0 or bullet.map_position.y < 0

    def __add_monster(self):
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

    def get_screen_position(self, sth):
        return Vector2(sth.map_position.x - self.camera_position.x, sth.map_position.y - self.camera_position.y)

    def is_on_screen(self, sth):
        return 0 < self.get_screen_position(sth).x + sth.size.x \
               and self.get_screen_position(sth).x < self.__screen_size.x \
               and 0 < self.get_screen_position(sth).y + sth.size.x \
               and self.get_screen_position(sth).y < self.__screen_size.y

    def __get_cords_in_array(self, v):
        return Vector2(v.x // self.__chunk_size, v.y // self.__chunk_size)

    def keep_no_monsters(self):
        no_needed_monsters = self.__min_no_monsters - len(self.__monsters)
        if no_needed_monsters > 0:
            for i in range(no_needed_monsters):
                self.__add_monster()

    def increase_min_no_monsters(self, num):
        self.__min_no_monsters += num

    def check_collisions(self):
        monster_h = Monster.size.y * 2 / 5
        hero_h = self.__hero.size.y * 2 / 5
        bullet_h = Bullet.size.y * 2 / 5
        grenade_h = Grenade.size.y * 2 / 5

        """hero grabs dropped item"""
        dist = self.__hero.size.x // 2
        for item in self.__dropped_items:
            if get_distance(self.__hero, item) < dist:
                self.__hero.pick_up_dropped_item(item)
                self.__dropped_items.remove(item)

        """bullet hits monster or tree"""
        for bullet in self.__bullets:
            if self.__bullet_hit_map_element(bullet.map_position):
                self.__bullets.remove(bullet)
            else:
                for monster in self.__monsters:
                    if get_distance(monster, bullet) < bullet_h + monster_h:
                        self.__bullets.remove(bullet)
                        monster.hurt(time(), bullet.damage)
                        if monster.hp <= 0:
                            dropped_item = monster.drop_item()
                            if dropped_item is not None:
                                self.__dropped_items.append(dropped_item)

                            self.__monsters.remove(monster)
                            self.__score += 1
                        break

        """grenades explode (time)"""
        now = time()
        grenade_time_to_explode = 2
        for grenade in self.__grenades:
            if now - grenade.create_time >= grenade_time_to_explode:
                self.__grenade_explodes(grenade)

        """grenade hits monster or tree"""
        for grenade in self.__grenades:
            if self.__bullet_hit_map_element(grenade.map_position):
                self.__grenade_explodes(grenade)
            else:
                for monster in self.__monsters:
                    if get_distance(monster, grenade) < grenade_h + monster_h:
                        self.__grenade_explodes(grenade)
                        break

        """monster attacks hero"""
        for monster in self.__monsters:
            if get_distance(self.__hero, monster) < monster_h + hero_h:
                if monster.last_attack == 0 or monster.last_attack + 1 < time():
                    monster.attack()
                    self.__hero.hurt(1)
        """bullet hits hero"""
        for bullet in self.__bullets:
            if get_distance(self.__hero, bullet) < bullet_h + hero_h:
                self.__bullets.remove(bullet)
                self.__hero.hurt(bullet.damage)

    def __grenade_explodes(self, grenade):
        for i in range(16):
            self.__bullets.append(Bullet(grenade.map_position, grenade.angle + (i + 1) * 22.5, 4))

        self.__grenades.remove(grenade)

    @property
    def camera_position(self):
        """get position of rectangle (cut out of background image) which will be shown on the screen"""
        camera_x = self.__hero.map_position.x - self.__hero.screen_position.x
        camera_y = self.__hero.map_position.y - self.__hero.screen_position.y
        return Vector2(camera_x, camera_y)

    @property
    def score(self):
        return self.__score

    @property
    def size(self):
        return self.__size

    @property
    def array(self):
        return self.__array

    @property
    def chunk_size(self):
        return self.__chunk_size

    @property
    def hero(self):
        return self.__hero

    @property
    def monsters(self):
        return self.__monsters

    @property
    def bullets(self):
        return self.__bullets

    @property
    def grenades(self):
        return self.__grenades

    @property
    def dropped_items(self):
        return self.__dropped_items
