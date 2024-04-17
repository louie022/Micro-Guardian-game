import pygame
from mover import Mover

class Microplastics(Mover):
    def __init__(self, x, y, vx, vy, m, image_path):
        super().__init__(x, y, vx, vy, m)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(center=(x, y))


    def update(self):
        # Call the superclass update to move the microplastics
        super().update()  

        # After updating position, update the rect to match the new position
        self.rect.x = self.pos.x - self.r * 2
        self.rect.y = self.pos.y - self.r * 2


    def show(self, screen):
        screen.blit(self.image, self.rect.topleft)
