import pygame
from settings import *
import time
import random
import math
from extraVectorFunctions import random2D, rotateVector
from mover import Mover
from microplastics import Microplastics
from garment import Garment

class Game:
    def __init__(self, surface, hand_manager):
        self.surface = surface
        
        # Load background
        self.background = pygame.image.load('Assets/Images/background2.png').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # load clothes image
        self.garment = Garment("Assets/Images/clothes.png", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 350, 0.01, 3)  # Adjust speed as needed

        # load clock
        self.clock = pygame.image.load("Assets/Images/clock.png")
        self.clock = pygame.transform.scale(self.clock, (50, 50))

        # load microplastic
        self.microplastic = pygame.image.load("Assets/Images/microplastic.png")
        self.microplastic = pygame.transform.scale(self.microplastic, (23, 23))

        # pre-load font
        font_path = "Assets/Font/PixelifySans-Medium.ttf"
        self.font_size = 36
        self.custom_font = pygame.font.Font(font_path, self.font_size)

        levelText_font_path = "Assets/Font/QuinqueFive.ttf"
        self.levelText_font_size = 24
        self.levelText_font = pygame.font.Font(levelText_font_path, self.levelText_font_size)

        number_font_path = "Assets/Font/QuinqueFive.ttf"
        self.number_font_size = 40
        self.number_font = pygame.font.Font(number_font_path, self.number_font_size)

        # Load camera & hand tracking
        self.hand_manager = hand_manager
        
        self.frame_count = 0

        # Get time
        self.last_spawn_time = pygame.time.get_ticks()

        self.particles = []

        ## difficulty variables
        self.spawn_interval = 2000  # Microplastic spawn interval in milliseconds
        self.microplastic_speed_range = (1, 2)  # moving speed
        self.microplastics_per_spawn = 1  # quantity per spawn_interval

        self.current_level = 1
        self.set_difficulty(self.current_level)

        self.collected_microplastics = 0


    def reset(self):
        self.particles = []
        self.generate_particles()

        self.sun = Mover(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 0, 0, 200)

        self.garment.angle = 0  # Reset garment position

        self.collected_microplastics = 0

        # initialise game time
        self.game_start_time = time.time()
        

    def game_time_update(self):
        self.time_left = max(round(GAME_DURATION - (time.time() - self.game_start_time), 1), 0)


    # generate particles: H2O, microplastics, etc.
    def generate_particles(self):
        # generate H2O, e.g. 100
        for i in range(100):
            pos = random2D()
            vel = pos
            vel = vel.normalize()
            vel.scale_to_length(random.uniform(2, 6))
            pos.scale_to_length(random.uniform(150, 250))
            vel = rotateVector(vel, math.pi / 2)
            m = 25
            self.particles.append(Mover(pos.x + SCREEN_WIDTH / 2, pos.y + SCREEN_HEIGHT / 2, vel.x, vel.y, m))
    

    def spawn_microplastics(self):
        current_time = pygame.time.get_ticks()

        # quantity per spawn_interval
        if (current_time - self.last_spawn_time >= self.spawn_interval):
            for _ in range(self.quantity_per_spawn):
                pos = random2D()
                vel = pos
                vel = vel.normalize()
                vel.scale_to_length(random.uniform(self.microplastic_speed_range[0], self.microplastic_speed_range[1]))
                pos.scale_to_length(random.uniform(250, 300)) # radius of trajectory
                vel = rotateVector(vel, math.pi / 2)
                # Assuming mass of microplastic
                m = 5
                self.particles.append(Microplastics(pos.x + SCREEN_WIDTH / 2, pos.y + SCREEN_HEIGHT / 2, vel.x, vel.y, m, "Assets/Images/microplastic.png"))
            self.last_spawn_time = current_time


    def update_particles(self):
        for mover in self.particles:
            self.sun.attract(mover)
            for other in self.particles:
                if mover != other:
                    mover.attract(other)

        for mover in self.particles:
            mover.update()
        
        self.collected_microplastics += self.hand_manager.hand.remove_colliding_microplastics(self.particles)


    def draw(self):
        ## 1. draw background
        self.surface.blit(self.background, (0, 0))

        ### draw circle as boundary
        self.draw_circle_boundary()
        
        # draw level message
        level_text = "Level"
        level_surface = self.levelText_font.render(level_text, True, (255, 255, 255))
        level_rect = level_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.surface.blit(level_surface, level_rect)

        number_text = f"{self.current_level}"
        number_surface = self.number_font.render(number_text, True, (255, 255, 255))
        number_rect = number_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.surface.blit(number_surface, number_rect)


        # draw clock
        self.surface.blit(self.clock, (SCREEN_WIDTH // 2 + 240, 200))

        ## 4. draw the remaining time
        if self.time_left < 5:  # change colour if only 5s left
            timer_text_colour = (255, 0, 0)  
        else: 
            timer_text_colour = (0, 255, 0)
        
        time_message = f"{self.time_left}"
        time_text_surface = self.custom_font.render(time_message, True, timer_text_colour)
        text_rect = time_text_surface.get_rect(topleft=(SCREEN_WIDTH // 2 + 290, 200))
        self.surface.blit(time_text_surface, text_rect)

        ## draw score
        self.surface.blit(self.microplastic, (SCREEN_WIDTH // 2 + 260, 270))
        
        collected_text = f"{self.collected_microplastics}"
        collected_text_surface = self.custom_font.render(collected_text, True, (255, 213, 39))
        collected_rect = collected_text_surface.get_rect(topleft=(SCREEN_WIDTH // 2 + 290, 260))
        self.surface.blit(collected_text_surface, collected_rect)


        ## 2. draw particles
        for mover in self.particles:
            mover.show(self.surface)

        ## draw garment
        self.garment.draw(self.surface)

        ## 3. draw hand
        self.hand_manager.draw_hand(self.surface)

        


    def update(self):
        ## hand position updating
        # Update hand tracking every N frames to reduce processing load
        self.frame_count += 1
        if self.frame_count % 5 == 0:  # Adjust N as needed
            self.hand_manager.update()
        # self.hand_manager.update()

        ## time updating
        self.game_time_update()

        ## update garment
        self.garment.update()

        if self.time_left > 0:
            ## generate microplastic
            self.spawn_microplastics()

            self.update_particles()

            # collect microplastics with hand
            self.hand_manager.hand.remove_colliding_microplastics(self.particles)
        else:
            return "game_over"

        self.draw()

    
    def set_difficulty(self, selected_level):
        self.current_level = selected_level

        if selected_level == 1:
            self.spawn_interval = 2000
            self.microplastic_speed_range = (1, 2)
            self.quantity_per_spawn = 1

        elif selected_level == 2:
            self.spawn_interval = 1500  # Shorter spawn interval
            self.microplastic_speed_range = (2, 4)  # Faster microplastics
            self.quantity_per_spawn = 3  # More microplastics per spawn

        elif selected_level == 3:
            self.spawn_interval = 1000
            self.microplastic_speed_range = (3, 6)
            self.quantity_per_spawn = 5

    
    def draw_circle_boundary(self):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        radius = SCREEN_WIDTH // 2
        color = (255, 255, 255)
        thickness = 1
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius, thickness)