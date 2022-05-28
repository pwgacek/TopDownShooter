import math
from pygame import Vector2, transform


def get_distance(obj1, obj2):
    x1, y1 = center_map_position(obj1)
    x2, y2 = center_map_position(obj2)

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def center_map_position(obj):
    return Vector2(obj.map_position.x + obj.size.x / 2, obj.map_position.y + obj.size.y / 2)


def get_rotated_image(image, angle):
    """ returns rotated  image while keeping its center and size"""

    orig_rect = image.get_rect()
    rot_image = transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def generate_images(image):
    return [get_rotated_image(image, angle) for angle in range(360)]


