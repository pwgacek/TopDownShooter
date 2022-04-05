import pygame
import math

from Hero import Hero


class Map:
    def __init__(self, w, h):
        self.width = 2000
        self.height = 2000
        self.window_width = w
        self.window_height = h
        self.image = pygame.image.load("assets/background.png")
        self.hero = Hero(pygame.math.Vector2(1000, 1000), pygame.math.Vector2(375, 275))

    def move_hero(self):
        move_speed = 0.3

        if (self.hero.get_dir()["down"] and self.hero.get_dir()["up"]) or not (self.hero.get_dir()["down"] or self.hero.get_dir()["up"]):
            change_y = 0
        elif self.hero.get_dir()["down"]:
            change_y = move_speed
        else:
            change_y = -move_speed
        if (self.hero.get_dir()["left"] and self.hero.get_dir()["right"]) or not (self.hero.get_dir()["left"] or self.hero.get_dir()["right"]):
            change_x = 0
        elif self.hero.get_dir()["left"]:
            change_x = -move_speed
        else:
            change_x = move_speed

        destination_x = self.hero.get_map_pos().x + change_x + self.hero.get_image().get_size()[0] / 2
        destination_y = self.hero.get_map_pos().y + change_y + self.hero.get_image().get_size()[1] / 2

        if change_x and change_y and self.can_move_to_y(destination_y):
            if self.can_move_to_x(destination_x):
                change_x /= math.sqrt(2)
                change_y /= math.sqrt(2)

        if self.can_move_to_x(destination_x):
            self.hero.get_map_pos().x += change_x
        if self.can_move_to_y(destination_y):
            self.hero.get_map_pos().y += change_y
        self.hero.set_angle()

    def get_camera_position(self):
        camera_x = self.hero.get_map_pos().x - self.hero.get_screen_pos().x
        camera_y = self.hero.get_map_pos().y - self.hero.get_screen_pos().y
        return camera_x, camera_y

    def can_move_to_x(self, x):
        if self.window_width / 2 < x < self.width - self.window_width / 2:
            return True
        return False

    def can_move_to_y(self, y):
        if self.window_height / 2 < y < self.height - self.window_height / 2:
            return True
        return False
