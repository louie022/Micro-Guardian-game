import math
import random
import pygame

def random2D():
    angle = random.uniform(0, 2 * math.pi)
    vector = pygame.math.Vector2(math.cos(angle), math.sin(angle))
    vector.normalize()
    return vector

def rotateVector(vector, angle):
    x, y = vector.x, vector.y
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    return pygame.math.Vector2(x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle)