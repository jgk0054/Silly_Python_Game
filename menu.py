import pygame
import sys
from constants import WIDTH, HEIGHT, WHITE, BLACK
from ship.shipyard import shipyard
def draw_text(screen, text, position, font, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def main_menu(screen):
    pygame.init()
    font = pygame.font.SysFont(None, 48)
    menu_options = ["Start Game", "Shipyard", "Exit"]
    selected_option = 0

    while True:
        screen.fill((0, 0, 0))

        # Draw the menu options
        for i, option in enumerate(menu_options):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            draw_text(screen, option, (WIDTH // 2 - 100, HEIGHT // 2 + i * 60), font, color)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Start Game
                        return "start"
                    elif selected_option == 1:  # Shipyard
                        shipyard(screen)
                    elif selected_option == 2:  # Exit
                        pygame.quit()
                        sys.exit()
