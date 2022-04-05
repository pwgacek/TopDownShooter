import pygame
import math

from Hero import Hero


class Map:
    def __init__(self, screen_size):
        self.width = 2000
        self.height = 2000
        self.screen_size = screen_size
        self.image = pygame.image.load("assets/background2.jpg")
        self.hero = Hero(pygame.math.Vector2(self.width/2, self.height/2), self.screen_size)

    def move_hero(self, flag_up, flag_down, flag_left, flag_right):
        move_speed = 0.3

        if (flag_down and flag_up) or not (flag_down or flag_up):
            change_y = 0
        elif flag_down:
            change_y = move_speed
        else:
            change_y = -move_speed
        if (flag_left and flag_right) or not (flag_left or flag_right):
            change_x = 0
        elif flag_left:
            change_x = -move_speed
        else:
            change_x = move_speed

        destination_x = self.hero.map_position.x + change_x + self.hero.image.get_size()[0] / 2
        destination_y = self.hero.map_position.y + change_y + self.hero.image.get_size()[1] / 2

        if change_x and change_y and self.can_move_to_y(destination_y):
            if self.can_move_to_x(destination_x):
                change_x /= math.sqrt(2)
                change_y /= math.sqrt(2)

        if self.can_move_to_x(destination_x):
            self.hero.map_position.x += change_x
        if self.can_move_to_y(destination_y):
            self.hero.map_position.y += change_y
        self.hero.set_angle()

    def get_camera_position(self):
        camera_x = self.hero.map_position.x - self.hero.screen_position.x
        camera_y = self.hero.map_position.y - self.hero.screen_position.y
        return camera_x, camera_y

    def can_move_to_x(self, x):
        if self.screen_size.x / 2 < x < self.width - self.screen_size.x / 2:
            return True
        return False

    def can_move_to_y(self, y):
        if self.screen_size.y / 2 < y < self.height - self.screen_size.y / 2:
            return True
        return False
