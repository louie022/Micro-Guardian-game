import pygame
from settings import *

class Button:
    def __init__(self, x, y, default_image, triggered_image, scale):
        self.x = x
        self.y = y
        self.default_image = pygame.transform.scale(default_image, (int(default_image.get_width() * scale), int(default_image.get_height() * scale)))
        self.triggered_image = pygame.transform.scale(triggered_image, (int(triggered_image.get_width() * scale), int(triggered_image.get_height() * scale)))
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.isTriggered = False

        self.trigger_sound = pygame.mixer.Sound("Assets/Audio/button_sound.mp3")
        self.trigger_sound.set_volume(SOUNDS_VOLUMN)

    # def set_hover(self, hover):
    #     self.image = self.hover_image if hover else self.default_image

    def reset_state(self):
        self.isTriggered = False
        self.image = self.default_image


    def draw(self, surface):
        # draw button on screen
        if self.isTriggered:
            self.rect.topleft = (self.x, self.y + self.default_image.get_height() - self.triggered_image.get_height())
        else:
            self.rect.topleft = (self.x, self.y)
        
        surface.blit(self.image, (self.rect.x, self.rect.y))

    
    def check_click(self, position, hand_closed):
        if self.rect.collidepoint(position) and hand_closed:
            self.isTriggered = not self.isTriggered  # Toggle state on click

            self.trigger_sound.play()

            # Update the button's appearance based on its state
            self.image = self.triggered_image if self.isTriggered else self.default_image
            return True
        return False