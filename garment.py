import pygame
import math

class Garment:
    def __init__(self, image_path, center, radius, speed, scale_factor):
        self.original_image = pygame.image.load(image_path).convert_alpha()  # Load the garment image
        self.image = pygame.transform.rotozoom(self.original_image, 0, scale_factor)  # Scale the image
        self.center = center  # Center of the circle (x, y)
        self.radius = radius  # Radius of the circular path
        self.speed = speed  # Speed of movement (radians per frame)
        self.angle = 0  # Current angle in radians
        self.scale_factor = scale_factor

    def update(self):
        # Update the angle for the next frame
        self.angle += self.speed
        self.angle %= 2 * math.pi  # Keep the angle within a range of 0 to 2π

        # Calculate the new position based on the center, radius, and angle
        self.pos_x = self.center[0] + math.cos(self.angle) * self.radius
        self.pos_y = self.center[1] + math.sin(self.angle) * self.radius

        # Calculate the rotation of the garment
        # The garment image points upwards initially, so we offset the rotation by 90 degrees (-90)
        # to ensure it follows the path correctly with the top facing the movement direction.
        rotation_angle = math.degrees(self.angle) - 90
        self.rotated_image = pygame.transform.rotozoom(self.original_image, -rotation_angle, self.scale_factor)

    def draw(self, surface):
        # Calculate the new position to draw the image, taking into account the rotation
        image_rect = self.rotated_image.get_rect(center=(self.pos_x, self.pos_y))
        surface.blit(self.rotated_image, image_rect)