import numpy as np
import random

import pygame
from PIL import Image, ImageDraw
from math import atan2
from random import randint
from pygame import Vector2


def __generate_vertexes(no_vertexes, height, width, x_space, y_space):
    """generates [no_vertexes] vertexes of  convex polygon using Valtr algorithm"""

    xs = [randint(x_space, width - x_space) for _ in range(no_vertexes)]
    ys = [randint(y_space, height - y_space) for _ in range(no_vertexes)]

    xs = sorted(xs)
    ys = sorted(ys)

    min_x, *xs, max_x = xs
    min_y, *ys, max_y = ys

    vectors_xs = __generate_vectors_coordinates(xs, min_x, max_x)
    vectors_ys = __generate_vectors_coordinates(ys, min_y, max_y)

    random.shuffle(vectors_ys)

    def to_vector_angle(vector):
        x, y = vector
        return atan2(y, x)

    vectors = sorted(zip(vectors_xs, vectors_ys), key=to_vector_angle)

    point_x = point_y = 0
    min_polygon_x = min_polygon_y = 0
    points = []

    for vector_x, vector_y in vectors:
        points.append((point_x, point_y))
        point_x += vector_x
        point_y += vector_y
        min_polygon_x = min(min_polygon_x, point_x)
        min_polygon_y = min(min_polygon_y, point_y)

    shift_x = min_x - min_polygon_x
    shift_y = min_y - min_polygon_y

    return [(point_x + shift_x, point_y + shift_y) for point_x, point_y in points]


def __generate_vectors_coordinates(coordinates, min_coordinate, max_coordinate):
    last_min = last_max = min_coordinate
    result = []
    for coordinate in coordinates:
        if randint(0, 1):
            result.append(coordinate - last_min)
            last_min = coordinate
        else:
            result.append(last_max - coordinate)
            last_max = coordinate

    result.extend((max_coordinate - last_min, last_max - max_coordinate))
    return result


def generate_array(no_vertexes, map_height, map_width, chunk_size, screen_size):
    polygon = __generate_vertexes(no_vertexes, map_height / chunk_size, map_width / chunk_size,
                                  (screen_size.x / chunk_size) / 2 + 3,
                                  (screen_size.y / chunk_size) / 2 + 3)

    img = Image.new('L', (int(map_width / chunk_size), int(map_height / chunk_size)), 0)
    ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
    return np.array(img)


def get_rotated_image(image, angle):
    """ returns rotated  image while keeping its center and size"""

    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def generate_background(chunk_size, map_size, array):
    tree_image = pygame.image.load("assets/tree3.png")
    background = pygame.Surface((map_size.x, map_size.y), pygame.SRCALPHA)
    width = int(map_size.x / chunk_size)
    height = int(map_size.y / chunk_size)

    shift = (tree_image.get_size()[0] - chunk_size) / 2
    for i in range(width):
        for j in range(height):
            if array[i][j] == 0:
                background.blit(get_rotated_image(tree_image, random.randint(0, 359)),
                                Vector2(i * chunk_size - shift, j * chunk_size - shift))

    return background


def generate_grass(chunk_size, map_size, array):
    grass = list()
    grass.append(pygame.image.load("assets/grass1.png"))
    grass.append(pygame.image.load("assets/grass2.png"))
    grass.append(pygame.image.load("assets/grass3.png"))

    grassland = pygame.Surface((map_size.x, map_size.y), pygame.SRCALPHA)
    width = int(map_size.x / chunk_size)
    height = int(map_size.y / chunk_size)
    # print(width, height)
    for i in range(width):
        for j in range(height):
            if array[i][j] == 1:
                k = randint(0, 150)
                if k < 3:
                    grassland.blit(get_rotated_image(grass[k], random.randint(0, 359)),
                                   Vector2(i * chunk_size, j * chunk_size))

    return grassland
