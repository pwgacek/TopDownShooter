import numpy as np
import random

import pygame
from PIL import Image, ImageDraw
from math import atan2
from random import randint
from pygame import Vector2
from src.utilities.Utils import get_rotated_image


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


def generate_array(no_vertexes,  map_width, map_height, chunk_size, screen_size):
    polygon = __generate_vertexes(no_vertexes, map_height / chunk_size, map_width / chunk_size,
                                  (screen_size.x / chunk_size) / 2 + 3, (screen_size.y / chunk_size) / 2 + 3)

    img = Image.new('L', (int(map_width / chunk_size), int(map_height / chunk_size)), 0)
    ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
    return np.array(img)


def generate_borders(chunk_size, map_size, array):
    tree_image = pygame.image.load("../assets/tree3.png")
    borders = pygame.Surface((map_size.x, map_size.y), pygame.SRCALPHA)
    width = int(map_size.x / chunk_size)
    height = int(map_size.y / chunk_size)

    shift = (tree_image.get_size()[0] - chunk_size) / 2
    for i in range(width):
        for j in range(height):
            if array[i][j] == 0:
                borders.blit(get_rotated_image(tree_image, random.randint(0, 359)),
                             Vector2(i * chunk_size - shift, j * chunk_size - shift))

    return borders


def generate_grass(chunk_size, map_size, array):
    grass = list()
    grass.append(pygame.image.load("../assets/grass1.png"))
    grass.append(pygame.image.load("../assets/grass2.png"))
    grass.append(pygame.image.load("../assets/grass3.png"))

    grassland = pygame.Surface((map_size.x, map_size.y), pygame.SRCALPHA)
    width = int(map_size.x / chunk_size)
    height = int(map_size.y / chunk_size)

    for i in range(width):
        for j in range(height):
            if array[i][j] == 1:
                k = randint(0, 150)
                if k < 3:
                    grassland.blit(get_rotated_image(grass[k], random.randint(0, 359)),
                                   Vector2(i * chunk_size, j * chunk_size))

    return grassland


def generate_map_elements(chunk_size, map_size, array):
    tree_image = pygame.image.load("../assets/tree3.png")
    shift = (tree_image.get_size()[0] - chunk_size) / 2

    big_tree = pygame.Surface((2 * chunk_size + shift, 2 * chunk_size + 2 * shift), pygame.SRCALPHA)
    """merging four trees into one big tree"""
    big_tree.blit(get_rotated_image(tree_image, randint(0, 359)), Vector2(0, 0))
    big_tree.blit(get_rotated_image(tree_image, randint(0, 359)), Vector2(chunk_size - shift, 0))
    big_tree.blit(get_rotated_image(tree_image, randint(0, 359)), Vector2(0, chunk_size - shift))
    big_tree.blit(get_rotated_image(tree_image, randint(0, 359)), Vector2(chunk_size - shift, chunk_size - shift))

    map_elements = pygame.Surface((map_size.x, map_size.y), pygame.SRCALPHA)

    width = int(map_size.x / chunk_size)
    height = int(map_size.y / chunk_size)

    middle_x = width // 2
    middle_y = height // 2

    def at_hero_starting_pos(a, b):
        return a == middle_x or a == middle_x + 1 or b == middle_y or b == middle_y + 1

    def can_place_big_tree(a, b):
        for k in range(-1, 3):
            for m in range(-1, 3):
                if array[a + k][b + m] == 0 and not at_hero_starting_pos(a + k, b + m):
                    return False

        return True

    available_places_list = list()

    for i in range(1, width - 2, 2):
        for j in range(1, height - 2, 2):
            if can_place_big_tree(i, j):
                available_places_list.append((i, j))

    for _ in range(min(40, len(available_places_list) // 2)):
        index = randint(0, len(available_places_list) - 1)
        x, y = available_places_list.pop(index)
        array[x][y] = array[x + 1][y] = array[x][y + 1] = array[x + 1][y + 1] = 2

        map_elements.blit(big_tree,
                          Vector2(x * chunk_size - shift, y * chunk_size - shift))

    return map_elements
