import pygame
import sys
from settings import *
from menu import Menu
from option import Option
from game import Game
from gameOver import GameOver
from microplastics import Microplastics
from handManager import HandManager
from potController import PotController

# Setup pygame/window --------------------------------------------- #
pygame.init()
pygame.display.set_caption('Micro Guardian')
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

hand_manager = HandManager()
pot_controller = PotController('COM4', 9600, 10)  # set up potentiometer

pygame.mixer.music.load("Assets/Audio/gameMusic.mp3")
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)


# initialise state of the game ------------------------------------- #
state = "menu"


# Creating screens ------------------------------------------------- #
menu = Menu(SCREEN)
option = Option(SCREEN, hand_manager)
game = Game(SCREEN, hand_manager)
game_over = GameOver(SCREEN, hand_manager)


# Game Functions --------------------------------------------------- #
def user_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pot_controller.close()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pot_controller.close()
                pygame.quit()
                sys.exit()

def update():
    global state

    if state == "menu":
        if pot_controller.update():
            game_level = pot_controller.get_game_level()
            option.set_level(game_level)
            hand_manager.full_reset()
            state = "option"
            # pot_controller.reset()
        menu.update()

    elif state == "option":
        transition = option.update()
        if transition == "game":
            selected_level = pot_controller.get_game_level()  # Get the selected game level
            game.set_difficulty(selected_level)  # Set the game level
            hand_manager.full_reset()
            game.reset()
            state = "game"

        elif transition == "menu":
            # reset the potController to avoid immediate re-triggering
            pot_controller.reset()
            state = "menu"
            hand_manager.full_reset()
            option.reset()

    elif state == "game":
        game_state = game.update()
        if game_state == "game_over":
            remaining_microplastics = sum(isinstance(p, Microplastics) for p in game.particles)
            game_over.set_remaining_microplastics(remaining_microplastics)
            hand_manager.full_reset()
            game_over.set_last_level_played(game.current_level)
            state = "game_over"
    
    elif state == "game_over":
        transition_back, next_level = game_over.update()
        if transition_back == "game":
            game_over.reset()
            hand_manager.full_reset()
            print("Restarting game at level:", next_level)  # Debug line
            game.set_difficulty(next_level)
            game.reset()
            state = "game"
        elif transition_back == "menu":
            game_over.reset()
            hand_manager.full_reset()
            game.reset()
            pot_controller.reset()
            state = "menu"
    
    #flip the screen?
    flipped_screen = pygame.transform.flip(SCREEN, True, False)  # Flip horizontally, not vertically
    SCREEN.blit(flipped_screen, (0, 0))

    pygame.display.update()
    

# Game Loop ------------------------------------------------------- #
running = True
while running:
    # whether exit
    user_events()

    # Update
    update()

    clock.tick(FPS)