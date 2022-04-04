import math

import pygame.font
from config import *
from functools import lru_cache


def clamp(value, mini, maxi):
    """Clamp value between mini and maxi"""
    if value < mini:
        return mini
    elif maxi < value:
        return maxi
    else:
        return value


def distance(p1, p2):
    """Get distance between 2 points"""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def map_to_range(value, from_x, from_y, to_x, to_y):
    """map the value from one range to another"""
    return clamp(value * (to_y - to_x) / (from_y - from_x), to_x, to_y)


@lru_cache(maxsize=100)
def text(msg, size=50, color=(255, 255, 255)):
    # return pygame.font.SysFont('consolas', size).render(msg, False, color)
    return pygame.font.Font(os.path.join(ASSETS, 'ARCADECLASSIC.TTF'), size).render(msg, False, color)
