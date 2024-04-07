import pygame
from microplastics import Microplastics
from settings import *

class Hand:
    def __init__(self):
        # create hand
        self.hand_image = pygame.image.load("Assets/Images/hand.png")
        # hand_new_size = (self.hand_image.get_width() // 2, self.hand_image.get_height() // 2)
        # self.hand_image = pygame.transform.scale(self.hand_image, hand_new_size)

        # initialise the value
        self.image = self.hand_image.copy()

        # create fist
        self.fist_image = pygame.image.load("Assets/Images/fist.png")
        # fist_new_size = (self.fist_image.get_width() // 2, self.fist_image.get_height() // 2)
        # self.fist_image = pygame.transform.scale(self.fist_image, fist_new_size)

        # self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, HAND_HITBOX_SIZE[0] / 2, HAND_HITBOX_SIZE[1] / 2)
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, HAND_HITBOX_SIZE[0], HAND_HITBOX_SIZE[1])
        self.left_click = False

        self.collect_sound = pygame.mixer.Sound("Assets/Audio/pop.mp3")
        self.collect_sound.set_volume(SOUNDS_VOLUMN)


    def draw(self, surface):
        # centre mode
        pos = list(self.rect.center)
        pos[0] -= self.image.get_width() // 2
        pos[1] -= self.image.get_height() // 2
        surface.blit(self.image, pos)

        # # draw the hand area
        # temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        # # Define the rectangle color with an alpha value (e.g., 128 for semi-transparency)
        # rect_color = (255, 0, 0, 128)
        # # Draw the semi-transparent rectangle on the temporary surface
        # pygame.draw.rect(temp_surface, rect_color, temp_surface.get_rect())
        # # Blit the temporary surface onto the main surface, positioned at self.rect's top-left corner
        # surface.blit(temp_surface, self.rect.topleft)

    
    def remove_colliding_microplastics(self, particles):
        initial_count = len(particles)
        if self.left_click:
            before_removal = len(particles)
            # Filter
            particles[:] = [p for p in particles if not self.check_collision(p)]
            after_removal = len(particles)

            removed_count = initial_count - len(particles)
            
            if before_removal > after_removal:
                self.collect_sound.play()
            
            return removed_count
        else:
            return 0


    def check_collision(self, particle):
        # Check if the particle is an instance of Microplastics
        if isinstance(particle, Microplastics):  
            return self.rect.colliderect(particle.rect)
        return False