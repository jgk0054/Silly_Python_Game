import pygame
from constants import WIDTH, HEIGHT
from menu import main_menu
from game import game_loop

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Solar System")
    
    while True:
        menu_choice = main_menu(screen)
        if menu_choice == "start":
            game_loop(screen)

if __name__ == "__main__":
    main()
