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

        if (self.hero.dir["down"] and self.hero.dir["up"]) or not (self.hero.dir["down"] or self.hero.dir["up"]):
            change_y = 0
        elif self.hero.dir["down"]:
            change_y = move_speed
        else:
            change_y = -move_speed
        if (self.hero.dir["left"] and self.hero.dir["right"]) or not (self.hero.dir["left"] or self.hero.dir["right"]):
            change_x = 0
        elif self.hero.dir["left"]:
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
        if self.window_width / 2 < x < self.width - self.window_width / 2:
            return True
        return False

    def can_move_to_y(self, y):
        if self.window_height / 2 < y < self.height - self.window_height / 2:
            return True
        return False
