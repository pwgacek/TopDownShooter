import pygame
from pygame.math import Vector2
import math

class Bullet:
    def __init__(self, map_position, angle, screen_size):
        self.map_position = map_position
        self.angle = angle
        self.image = pygame.transform.rotate(pygame.image.load("assets/bullet.png"), angle-90)
        self.screen_position = Vector2(screen_size.x / 2 - self.image.get_size()[0] / 2 + math.cos(math.radians(angle-14))*50,
                                         screen_size.y / 2 - self.image.get_size()[1] / 2 - math.sin(math.radians(angle-14))*50)


    def update_screen_pos(self, x, y):

        self.screen_position = Vector2(self.screen_position[0]- x, self.screen_position[1]-y)

    def move(self):
        speed = 20
        x1 = math.cos(math.radians(self.angle))
        y1 = math.sin(math.radians(self.angle))
        x = self.screen_position[0] + x1*speed
        y = self.screen_position[1] - y1*speed
        a = self.map_position[0] + x1*speed
        b = self.map_position[0] - y1*speed
        self.screen_position = Vector2(x, y)
        self.map_position = Vector2(a, b)



