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

    def move_hero(self, flag_up, flag_down, flag_left, flag_right):

        if (flag_down and flag_up) or not (flag_down or flag_up):
            change_y = 0
        elif flag_down:
            change_y = 0.5
        else:
            change_y = -0.5
        if (flag_left and flag_right) or not (flag_left or flag_right):
            change_x = 0
        elif flag_left:
            change_x = -0.5
        else:
            change_x = 0.5


        if change_x and change_y and self.can_move_to_y(self.hero.map_position.y + change_y):
            if self.can_move_to_x(self.hero.map_position.x + change_x) :
                change_x /= math.sqrt(2)
                change_y /= math.sqrt(2)

        if self.can_move_to_x(self.hero.map_position.x + change_x):
            self.hero.map_position.x += change_x
        if self.can_move_to_y(self.hero.map_position.y + change_y):
            self.hero.map_position.y += change_y


    def get_camera_position(self):
        camera_x = self.hero.map_position.x - self.hero.screen_position.x
        camera_y = self.hero.map_position.y - self.hero.screen_position.y
        return camera_x, camera_y

    def can_move_to_x(self, x):
        if x > self.window_width/2 and x < self.width - self.window_width/2:

            return True
        return False

    def can_move_to_y(self, y):
        if y > self.window_height / 2  and y < self.height - self.window_height/2:
            return True
        return False