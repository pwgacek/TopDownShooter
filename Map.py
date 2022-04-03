import pygame

from Hero import Hero


class Map:
    def __init__(self):
        self.width = 2000
        self.height = 2000
        self.image = pygame.image.load("assets/background.png")
        self.hero = Hero(pygame.math.Vector2(1000, 1000), pygame.math.Vector2(375, 275))

    def move_hero(self, flag_up, flag_down, flag_left, flag_right):

        if (flag_down and flag_up) or not (flag_down or flag_up):
            change_y = 0
        elif flag_down:
            change_y = 0.1
        else:
            change_y = -0.1
        if (flag_left and flag_right) or not (flag_left or flag_right):
            change_x = 0
        elif flag_left:
            change_x = -0.1
        else:
            change_x = 0.1

        self.hero.map_position.x += change_x
        self.hero.map_position.y += change_y
        self.hero.set_angle()

    def get_camera_position(self):
        camera_x = self.hero.map_position.x - self.hero.screen_position.x
        camera_y = self.hero.map_position.y - self.hero.screen_position.y
        return camera_x, camera_y
