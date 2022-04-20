import pygame
import math

from Hero import Hero
from Monster import Monster
from pygame.math import Vector2
from Bullet import Bullet
from random import randint



class Map:
    def __init__(self, screen_size):
        self.__width = 2000
        self.__height = 2000
        self.__screen_size = screen_size
        self.__image = pygame.image.load("assets/background2.jpg")
        self.__hero = Hero(Vector2(self.__width / 2, self.__height / 2), self.__screen_size)
        self.__bullets = list()
        self.__font = pygame.font.SysFont('Bradley Hand ITC', 50, bold = pygame.font.Font.bold)
        self.__monsters = list()


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

        destination_x = self.__hero.get_map_position().x + change_x + self.__hero.get_image().get_size()[0] / 2
        destination_y = self.__hero.get_map_position().y + change_y + self.__hero.get_image().get_size()[1] / 2

        """maintain speed when moving diagonally"""
        if change_x and change_y and self.__can_move_to_y(destination_y) and self.__can_move_to_x(destination_x):
            change_x /= math.sqrt(2)
            change_y /= math.sqrt(2)

        """change position if possible"""
        if self.__can_move_to_x(destination_x):
            self.__hero.get_map_position().x += change_x
        if self.__can_move_to_y(destination_y):
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

    def __can_move_to_x(self, x):
        return self.__screen_size.x / 2 < x < self.__width - self.__screen_size.x / 2

    def __can_move_to_y(self, y):
        return self.__screen_size.y / 2 < y < self.__height - self.__screen_size.y / 2

    def get_image(self):
        return self.__image

    def get_hero(self):
        return self.__hero

    def add_bullet(self):
        self.__hero.set_ammo(self.__hero.get_ammo() -1)
        a = self.__hero.get_map_position()[0]
        b = self.__hero.get_map_position()[1]

        x = pygame.math.Vector2(a, b)
        y = self.__hero.get_angle()
        if y >= 270:
            y -= 270
        else:
            y += 90
        z = self.__screen_size
        self.__bullets.append(Bullet(x, y, z))

    def update_bullets(self, camera_x, camera_y):
        for i in self.__bullets:
            i.update_screen_pos(camera_x, camera_y)

    def move_bullets(self):
        for i in self.__bullets:
            i.move()

    def remove_bullets(self):
        for i in self.__bullets:
            if self.bullet_not_in_bounds(i):
                self.__bullets.remove(i)

    def bullet_not_in_bounds(self, bullet):
        return  bullet.get_map_position()[0] > 2000 or bullet.get_map_position()[1] > 2000 or bullet.get_map_position()[0] < 0 or bullet.get_map_position()[1] < 0

    def show_ammo(self):
        return self.__font.render("Ammo: "+ str(self.__hero.bullets) + "  reload (r)", True, (255, 0, 0))

    def get_monsters(self):
        return self.__monsters

    def get_bullets(self):
        return self.__bullets

    def get_font(self):
        return self.__font

    def show_ammo2(self, screen):
        x = 20
        for i in range(self.__hero.get_ammo()):
            screen.blit(pygame.image.load("assets/ammo1.png"), (x, 520))
            x += 41
        screen.blit(self.__font.render("Reload (r)", True, (255, 0, 0)), (400, 530))


    def add_monster(self):
        x = randint(0, self.__width)
        y = randint(0, self.__height)
        self.__monsters.append(Monster(Vector2(x, y)))

    def __remove_monster(self, monster):
        self.__monsters.remove(monster)

