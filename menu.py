import pygame
from settings import *

class Menu:
    def __init__(self, surface):
        self.surface = surface

        ### 1. Load background
        self.background = pygame.image.load('Assets/Images/background2.png').convert()

        # Get the original dimensions of the background
        self.bg_width, self.bg_height = self.background.get_size()

        # Calculate the scaling factor while making sure the entire screen is covered
        self.scale_width = SCREEN_WIDTH / self.bg_width
        self.scale_height = SCREEN_HEIGHT / self.bg_height
        self.scale_factor = max(self.scale_width, self.scale_height)  # Use max to ensure the image covers the entire screen

        # Scale the image using the calculated scale factor
        self.new_bg_size = (int(self.bg_width * self.scale_factor), int(self.bg_height * self.scale_factor))
        self.background = pygame.transform.scale(self.background, self.new_bg_size)

        # Calculate position to center the image (this will crop the excess part of the image)
        self.bg_x = (SCREEN_WIDTH - self.new_bg_size[0]) // 2
        self.bg_y = (SCREEN_HEIGHT - self.new_bg_size[1]) // 2

        # Load frames
        self.frames = []
        self.load_frames()
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.frame_rate = 200
  

    def load_frames(self):
        frame_path = [
            "Assets/Images/frame1.png",
            "Assets/Images/frame2.png",
            "Assets/Images/frame3.png",
            "Assets/Images/frame4.png",
            "Assets/Images/frame5.png"
        ]
        for path in frame_path:
            image = pygame.image.load(path).convert_alpha()
            self.frames.append(image)


    def draw(self):
        ### 1. draw background
        self.surface.blit(self.background, (self.bg_x, self.bg_y))

        ### draw circle as boundary
        self.draw_circle_boundary()

        ### 3. loop frames
        frame = self.frames[self.current_frame]
        frame_rect = frame.get_rect()
        centered_x = (SCREEN_WIDTH - frame_rect.width) // 2
        centered_y = (SCREEN_HEIGHT - frame_rect.height) // 2
        self.surface.blit(frame, (centered_x, centered_y))
    
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update_time = current_time

        # draw menu screen content
        self.draw()


    def draw_circle_boundary(self):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        radius = SCREEN_WIDTH // 2
        color = (255, 255, 255)
        thickness = 1
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius, thickness)