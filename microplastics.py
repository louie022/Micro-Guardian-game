import pygame
from mover import Mover

class Microplastics(Mover):
    def __init__(self, x, y, vx, vy, m, image_path):
        super().__init__(x, y, vx, vy, m)
        self.image = pygame.image.load(image_path).convert_alpha()
        # self.rect = pygame.Rect(self.pos.x, self.pos.y, self.r * 4, self.r * 4)
        self.image = pygame.transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(center=(x, y))


    def update(self):
        # Call the superclass update to move the microplastics
        super().update()  

        # After updating position, update the rect to match the new position
        self.rect.x = self.pos.x - self.r * 2
        self.rect.y = self.pos.y - self.r * 2


    def show(self, screen):
        # rect_top_left = (self.pos.x - self.r * 2, self.pos.y - self.r * 2)
        # pygame.draw.rect(screen, (255, 0, 0), (*rect_top_left, self.r * 4, self.r * 4))
        screen.blit(self.image, self.rect.topleft)

        # self.draw_hitbox(screen)


    # def draw_hitbox(self, surface):
    #     pygame.draw.rect(surface, (200, 60, 120), self.rect)