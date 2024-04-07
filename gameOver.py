import pygame
from settings import *
from button import Button

class GameOver:
    def __init__(self, surface, hand_manager):
        self.surface = surface

        # hand tracking
        self.hand_manager = hand_manager
        self.frame_count = 0

        # load background
        self.game_over_background = pygame.image.load('Assets/Images/background2.png').convert()
        self.game_over_background = pygame.transform.scale(self.game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # pre-load font
        font_path = "Assets/Font/QuinqueFive.ttf"
        self.font_size = 48
        self.custom_font = pygame.font.Font(font_path, self.font_size)

        number_font_path = "Assets/Font/QuinqueFive.ttf"
        self.number_font_size = 72
        self.number_font = pygame.font.Font(number_font_path, self.number_font_size)

        regular_font_path = "Assets/Font/PixelifySans-Regular.ttf"
        self.regular_font_size = 48
        self.regular_font = pygame.font.Font(regular_font_path, self.regular_font_size)

        # load exit button
        yes_default_image = pygame.image.load("Assets/Images/yes.png").convert_alpha()
        yes_triggered_image = pygame.image.load("Assets/Images/yes.png").convert_alpha()
        exit_default_image = pygame.image.load("Assets/Images/exit.png").convert_alpha()
        exit_triggered_image = pygame.image.load("Assets/Images/exit.png").convert_alpha()

        self.yes_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 150, yes_default_image, yes_triggered_image, 1)
        self.exit_button = Button(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 150, exit_default_image, exit_triggered_image, 1)

        self.remaining_microplastics = 0
        self.last_level_played = 1


    def reset(self):
        self.yes_button.reset_state()
        self.exit_button.reset_state()
        self.hand_manager.reset_hand_position()
        # self.last_level_played = 1


    def set_remaining_microplastics(self, count):
        self.remaining_microplastics = count


    def set_last_level_played(self, level):
        self.last_level_played = level


    def draw(self):
        self.surface.blit(self.game_over_background, (0, 0))

        ### draw circle as boundary
        self.draw_circle_boundary()

        ## number text
        number_text = f"{self.remaining_microplastics}"
        number_text_surface = self.custom_font.render(number_text, True, (255, 255, 255))
        number_text_rect = number_text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.surface.blit(number_text_surface, number_text_rect)

        # level_surface = self.levelText_font.render(level_text, True, (255, 255, 255))
        # level_rect = level_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        # self.surface.blit(level_surface, level_rect)

        # number_text = f"{self.current_level}"
        # number_surface = self.number_font.render(number_text, True, (255, 255, 255))
        # number_rect = number_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        # self.surface.blit(number_surface, number_rect)

        game_over_message = "microplastics remaining"
        text_surface = self.regular_font.render(game_over_message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.surface.blit(text_surface, text_rect)

        ### takeaway message 1
        takeaway_message_1 = "Choose natural fabrics"
        textaway_message1_surface = self.regular_font.render(takeaway_message_1, True, (255, 213, 39))
        takeaway_message1_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 370))
        self.surface.blit(textaway_message1_surface, takeaway_message1_rect)

        ### takeaway message 2
        takeaway_message_2 = "to reduce microplastic pollution"
        textaway_message2_surface = self.regular_font.render(takeaway_message_2, True, (255, 213, 39))
        takeaway_message2_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2 - 100, 435))
        self.surface.blit(textaway_message2_surface, takeaway_message2_rect)

        ### Do you want to try again?
        game_over_message = "play another level?"
        text_surface = self.regular_font.render(game_over_message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        self.surface.blit(text_surface, text_rect)

        self.yes_button.draw(self.surface)
        self.exit_button.draw(self.surface)

        self.hand_manager.draw_hand(self.surface)


    def update(self):
        # self.hand_manager.update()
        ## hand position updating
        # Update hand tracking every N frames to reduce processing load
        self.frame_count += 1
        if self.frame_count % 5 == 0:  # Adjust N as needed
            self.hand_manager.update()

        self.draw()

        # Get the current hand position
        hand_pos = self.hand_manager.hand.rect.center
        # Check if the hand is considered to be "clicking"
        hand_closed = self.hand_manager.hand.left_click

        # Check if the "yes" button is clicked
        if self.yes_button.check_click(hand_pos, hand_closed):
            print("Yes button clicked!")
            # back to game screen with certain difficulty
            next_level = self.calculate_next_level()
            print("next level:", next_level)
            return "game", next_level

        # Check if the "exit" button is clicked
        if self.exit_button.check_click(hand_pos, hand_closed):
            print("exit button clicked!")
            # return back to menu screen
            return "menu", None
        
        return None, None
        
    
    def calculate_next_level(self):
        if self.last_level_played in [1, 2]:
            return 3
        else:
            return 1


    def draw_circle_boundary(self):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        radius = SCREEN_WIDTH // 2
        color = (255, 255, 255)
        thickness = 1
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius, thickness)