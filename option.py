import pygame
from settings import *
from button import Button

class Option:
    def __init__(self, surface, hand_manager):
        self.surface = surface

        # set up the hand tracking & hand changes
        self.hand_manager = hand_manager
        self.frame_count = 0

        # Load background
        self.option_background = pygame.image.load('Assets/Images/background2.png').convert()
        self.option_background = pygame.transform.scale(self.option_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # pre-load font
        font_path_regular = "Assets/Font/PixelifySans-Regular.ttf"
        self.font_size_regular = 72
        self.regular_font = pygame.font.Font(font_path_regular, self.font_size_regular)

        font_path_bold = "Assets/Font/PixelifySans-Bold.ttf"
        self.font_size_bold = 84
        self.bold_font = pygame.font.Font(font_path_bold, self.font_size_bold)

        font_path_number = "Assets/Font/QuinqueFive.ttf"
        self.font_size_number = 60
        self.number_font = pygame.font.Font(font_path_number, self.font_size_number)

        font_path_caption = "Assets/Font/PixelifySans-Regular.ttf"
        self.font_size_caption = 42
        self.caption_font = pygame.font.Font(font_path_caption, self.font_size_caption)
        
        # Load images for the yes and no buttons for both states
        yes_default_image = pygame.image.load("Assets/Images/yes.png").convert_alpha()
        yes_triggered_image = pygame.image.load("Assets/Images/yes.png").convert_alpha()
        no_default_image = pygame.image.load("Assets/Images/no.png").convert_alpha()
        no_triggered_image = pygame.image.load("Assets/Images/no.png").convert_alpha()

        self.yes_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20, yes_default_image, yes_triggered_image, 1)
        self.no_button = Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 20, no_default_image, no_triggered_image, 1)

        # store the current game level
        self.current_game_level = None

        # Load frames
        self.grab_frames = []
        self.load_grab_frames()
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.frame_rate = 300

        # load microplastic
        self.microplastic = pygame.image.load("Assets/Images/microplastic.png")
        self.microplastic = pygame.transform.scale(self.microplastic, (23, 23))


    def load_grab_frames(self):
        frame_path = [
            "Assets/Images/hand.png",
            "Assets/Images/fist.png"
        ]
        for path in frame_path:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (image.get_width() * 0.5, image.get_height() * 0.5))
            self.grab_frames.append(image)


    def reset(self):
        self.yes_button.reset_state()
        self.no_button.reset_state()
        self.hand_manager.reset_hand_position()


    def set_level(self, game_level):
        self.current_game_level = game_level


    def draw(self):
        # 1. draw background
        self.surface.blit(self.option_background, (0, 0))

        ### draw circle as boundary
        self.draw_circle_boundary()

        # 2. draw game level message: This is game level 1/2/3
        # get value from pot and distribute the level
        if self.current_game_level is not None:
            level_message = "Game Level"
            level_text_surface = self.regular_font.render(level_message, True, (255, 255, 255))
            level_text_rect = level_text_surface.get_rect(center=(SCREEN_WIDTH / 2, 130))
            self.surface.blit(level_text_surface, level_text_rect)

            number_message = f"{self.current_game_level}"
            number_surface = self.number_font.render(number_message, True, (255, 255, 255))
            number_text_rect = number_surface.get_rect(center=(SCREEN_WIDTH / 2, 230))
            self.surface.blit(number_surface, number_text_rect)
            
        # 3. draw text: Are you ready?
        text_surface = self.bold_font.render("Are You Ready?", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2 - 70))
        self.surface.blit(text_surface, text_rect)

        ### 4. draw two option buttons
        self.yes_button.draw(self.surface)
        self.no_button.draw(self.surface)

        ### draw microplastics
        self.surface.blit(self.microplastic, (SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 + 175))

        ### 6. loop frames
        frame = self.grab_frames[self.current_frame]
        centered_x = SCREEN_WIDTH // 2 - 190
        centered_y = SCREEN_HEIGHT // 2 + 170
        self.surface.blit(frame, (centered_x, centered_y))

        ## draw caption
        caption_text_surface = self.caption_font.render("GRAB TO INTERACT", True, (255, 255, 255))
        caption_text_rect = caption_text_surface.get_rect(center=(SCREEN_WIDTH / 2 + 50, SCREEN_HEIGHT / 2 + 200))
        self.surface.blit(caption_text_surface, caption_text_rect)

        ### 5. draw hand
        self.hand_manager.draw_hand(self.surface)


    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.grab_frames)
            self.last_update_time = current_time

        # update hand tracking
        # self.hand_manager.update()
        self.frame_count += 1
        if self.frame_count % 5 == 0:  # Adjust N as needed
            self.hand_manager.update()

        # draw option screen
        self.draw()

        # Get the current hand position
        hand_pos = self.hand_manager.hand.rect.center
        # Check if the hand is considered to be "clicking"
        hand_closed = self.hand_manager.hand.left_click

        # Check if the "Yes" button is clicked
        if self.yes_button.check_click(hand_pos, hand_closed):
            print("Yes button clicked!")
            # Perform actions for "Yes" button click
            # This could involve changing the game state, loading a new screen, etc.
            return "game"

        # Check if the "No" button is clicked
        elif self.no_button.check_click(hand_pos, hand_closed):
            print("No button clicked!")
            # Perform actions for "No" button click
            return "menu"       
        # return None


    def draw_circle_boundary(self):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        radius = SCREEN_WIDTH // 2
        color = (255, 255, 255)
        thickness = 1
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius, thickness)