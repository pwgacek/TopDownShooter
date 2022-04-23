import pygame
import math

from Hero import Hero
from Monster import Monster
from pygame.math import Vector2
from Bullet import Bullet
from random import randint, random

from MapGenerator import generate_array, generate_background


class Map:
    def __init__(self, screen_size):
        self.__width = 4000
        self.__height = 4000
        self.__chunk_size = 50
        self.__screen_size = screen_size
        self.__array = generate_array(30, self.__height, self.__width, self.__chunk_size, self.__screen_size)
        self.__hero = Hero(Vector2(self.__width / 2, self.__height / 2), self.__screen_size)
        self.__bullets = list()
        self.__font = pygame.font.SysFont('Bradley Hand ITC', 50, bold=pygame.font.Font.bold)
        self.__monsters = list()
        self.__bullet_image = pygame.image.load("assets/ammo1.png")
        self.__tree_image = pygame.image.load("assets/tree3.png")
        self.__background = generate_background(self.__chunk_size, self.__tree_image,
                                                Vector2(self.__width, self.__height), self.__array)
        self.__min_no_monsters = 5

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
        if change_x and change_y and self.__can_move_to(Vector2(destination_x, destination_y)):
            change_x /= math.sqrt(2)
            change_y /= math.sqrt(2)

        """change position if possible"""
        if self.__can_move_to(Vector2(destination_x, current_y)):
            self.__hero.get_map_position().x += change_x
        if self.__can_move_to(Vector2(current_x, destination_y)):
            self.__hero.get_map_position().y += change_y

        self.__hero.set_angle()

    def move_monsters(self, move_speed):

        max_distance = self.__hero.get_image().get_size()[1] / 2
        for monster in self.__monsters:
            if math.dist(monster.get_map_position(), self.__hero.get_map_position()) > max_distance:

                x = monster.get_map_position().x + monster.get_unit_vector().x * move_speed
                y = monster.get_map_position().y + monster.get_unit_vector().y * move_speed

                xl = monster.get_map_position().x + monster.get_unit_vector(
                    (monster.get_angle() - 60) % 360).x * move_speed
                yl = monster.get_map_position().y + monster.get_unit_vector(
                    (monster.get_angle() - 60) % 360).y * move_speed

                xr = monster.get_map_position().x + monster.get_unit_vector(
                    (monster.get_angle() + 60) % 360).x * move_speed
                yr = monster.get_map_position().y + monster.get_unit_vector(
                    (monster.get_angle() + 60) % 360).y * move_speed

                can_move = True
                can_turn_left = True
                can_turn_right = True

                for other_monster in self.__monsters:
                    distance = math.dist(monster.get_map_position(), other_monster.get_map_position())

                    if other_monster != monster and distance < max_distance:
                        """Given monster can't go straight check if he turn left or right """

                        if distance >= math.dist(Vector2(x, y), other_monster.get_map_position()):
                            can_move = False
                        if distance >= math.dist(Vector2(xl, yl), other_monster.get_map_position()):
                            can_turn_left = False
                        if distance >= math.dist(Vector2(xr, yr), other_monster.get_map_position()):
                            can_turn_right = False

                        if not (can_move or can_turn_right or can_turn_left):
                            break

                """set new cords"""
                if can_move:
                    monster.get_map_position().x = x
                    monster.get_map_position().y = y

                elif can_turn_left:
                    monster.get_map_position().x = xl
                    monster.get_map_position().y = yl

                elif can_turn_right:
                    monster.get_map_position().x = xr
                    monster.get_map_position().y = yr

                monster.set_angle(self.__hero.get_map_position())

    def get_camera_position(self):
        """get position of rectangle (cut out of background image) which will be shown on the screen"""
        camera_x = self.__hero.get_map_position().x - self.__hero.get_screen_position().x
        camera_y = self.__hero.get_map_position().y - self.__hero.get_screen_position().y
        return Vector2(camera_x, camera_y)

    def __can_move_to(self, v):
        cords = self.__get_cords_in_array(v)
        return self.__array[int(cords.x)][int(cords.y)]

        # return self.__screen_size.x / 2 < x < self.__width - self.__screen_size.x / 2

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
            if self.bullet_not_in_bounds(i):
                self.__bullets.remove(i)

    def bullet_not_in_bounds(self, bullet):
        return bullet.get_map_position()[0] > self.__width or bullet.get_map_position()[1] > self.__height or \
               bullet.get_map_position()[0] < 0 or bullet.get_map_position()[1] < 0

    def get_monsters(self):
        return self.__monsters

    def get_bullets(self):
        return self.__bullets

    def get_font(self):
        return self.__font

    # screen.blit(self.__font.render("Reload (r)", True, (255, 0, 0)), (400, 530))

    def add_monster(self):
        if randint(0, 1):  # if True x = 0 or x = map_width
            if randint(0, 1):
                x = 0
            else:
                x = self.__width

            y = randint(0, self.__height)

        else:
            if randint(0, 1):
                y = 0
            else:
                y = self.__height

            x = randint(0, self.__width)

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

    # def get_array_elements_on_screen(self):
    #     pos = self.get_camera_position()
    #
    #     elements = list()
    #     for i in range(int(self.__screen_size.x / self.__chunk_size) + 1):
    #         start_vector = None
    #         counter = 0
    #         for j in range(int(self.__screen_size.y / self.__chunk_size) + 1):
    #             if self.__array[int(self.__get_cords_in_array(pos).x + i)][
    #                 int(self.__get_cords_in_array(pos).y + j)] == 0:
    #                 if start_vector is None:
    #                     start_vector = Vector2(self.__get_cords_in_array(pos).x + i,
    #                                            self.__get_cords_in_array(pos).y + j)
    #                 counter += 1
    #             else:
    #                 if start_vector is not None:
    #                     elements.append((start_vector, counter))
    #                     start_vector = None
    #                     counter = 0
    #
    #         if start_vector is not None:
    #             elements.append((start_vector, counter))
    #
    #             # elements.append(Vector2(self.__get_cords_in_array(pos).x + i, self.__get_cords_in_array(pos).y + j))
    #
    #     return elements

    # def get_tree_surface(self, num):
    #     return self.__tree_surfaces[num - 1]

    def get_chunk_size(self):
        return self.__chunk_size

    # def get_rotated_tree_image(self, angle):
    #     """ returns rotated  image while keeping its center and size"""
    #
    #     orig_rect = self.__tree_image.get_rect()
    #
    #     rot_image = pygame.transform.rotate(self.__tree_image, angle)
    #     rot_rect = orig_rect.copy()
    #     rot_rect.center = rot_image.get_rect().center
    #     rot_image = rot_image.subsurface(rot_rect).copy()
    #     return rot_image

    def get_tree_image(self):
        return self.__tree_image

    def get_background(self):
        return self.__background

    def get_bullet_image(self):
        return self.__bullet_image

    def keep_no_monsters(self):
        no_needed_monsters = self.__min_no_monsters - len(self.__monsters)
        if no_needed_monsters > 0:
            for i in range(no_needed_monsters):
                self.add_monster()

    def increase_min_no_monsters(self, num):
        self.__min_no_monsters += num
