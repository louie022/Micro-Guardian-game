import pygame
import math

class Mover:
    def __init__(self, x, y, vx, vy, m):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(vx, vy)
        self.acc = pygame.math.Vector2(0, 0)
        self.mass = m
        self.r = math.sqrt(self.mass) * 1
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.r, self.r)

    def applyForce(self, force):
        f = force / self.mass
        self.acc += f

    def attract(self, mover):
        force = self.pos - mover.pos
        distanceSq = max(min(force.length_squared(), 1000), 100)
        G = 0.4
        strength = (G * self.mass * mover.mass) / distanceSq
        force.scale_to_length(strength)
        mover.applyForce(force)

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.acc = pygame.math.Vector2(0, 0)

    def show(self, screen):
        pygame.draw.circle(screen, (60, 180, 224), (int(self.pos.x), int(self.pos.y)), self.r)
        # self.draw_hitbox(screen)

    # def draw_hitbox(self, surface):
    #     pygame.draw.rect(surface, (200, 60, 120), self.rect)