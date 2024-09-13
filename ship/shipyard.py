import pygame
import sys
from ship.engine import Engine
from ship.cabin import Cabin
from ship.fuel_tank import FuelTank
from ship.radiator import Radiator
from ship.ship_saver import save_ship

def shipyard(screen):
    pygame.init()
    font = pygame.font.SysFont(None, 48)
    cabin = Cabin(300, 300)
    components = []
    current_component = None
    ship = [cabin]

    # Define buttons for creating new components
    button_width = 150
    button_height = 50
    buttons = {
        "Add Engine": pygame.Rect(10, 10, button_width, button_height),
        "Add Fuel Tank": pygame.Rect(10, 70, button_width, button_height),
        "Add Radiator": pygame.Rect(10, 130, button_width, button_height),
        "Save Ship": pygame.Rect(10, 190, button_width, button_height)
    }

    while True:
        screen.fill((0, 0, 0))

        # Draw buttons
        for button_text, button_rect in buttons.items():
            pygame.draw.rect(screen, (255, 255, 255), button_rect)
            text_surface = font.render(button_text, True, (0, 0, 0))
            screen.blit(text_surface, (button_rect.x + 5, button_rect.y + 5))

        # Move the current component if dragging
        if current_component:
            mx, my = pygame.mouse.get_pos()
            current_component.x = mx - current_component.width // 2
            current_component.y = my - current_component.height // 2

        # Draw the available components
        for component in components:
            component.draw(screen, camera=None, lander_x=0, lander_y=0, lander_angle=0, scale=1, show_snap_points=True)

        # Draw the current ship
        for part in ship:
            part.draw(screen, camera=None, lander_x=0, lander_y=0, lander_angle=0, scale=1, show_snap_points=True)

        # Draw the current component being dragged, if any
        if current_component:
            current_component.draw(screen, camera=None, lander_x=0, lander_y=0, lander_angle=0, scale=1, show_snap_points=True)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if clicking on a button
                    for button_text, button_rect in buttons.items():
                        if button_rect.collidepoint(event.pos):
                            if button_text == "Add Engine":
                                components.append(Engine(600, 600))
                            elif button_text == "Add Fuel Tank":
                                components.append(FuelTank(600, 600))
                            elif button_text == "Add Radiator":
                                components.append(Radiator(600, 600))
                            elif button_text == "Save Ship":
                                save_ship(ship)
                            break
                    else:
                        # Check if clicking on an available component
                        if not current_component:
                            for component in components:
                                if component.x <= event.pos[0] <= component.x + component.width and component.y <= event.pos[1] <= component.y + component.height:
                                    current_component = component
                                    break
                            # Check if clicking on a part of the ship (excluding the cabin)
                            if not current_component:
                                for part in ship:
                                    if part != cabin and part.x <= event.pos[0] <= part.x + part.width and part.y <= event.pos[1] <= part.y + part.height:
                                        current_component = part
                                        ship.remove(part)
                                        components.append(part)
                                        break
                        else:
                            # Check for snapping to another part in the ship
                            snapped = False
                            for part in ship:
                                for ap1 in current_component.get_attachment_points():
                                    for ap2 in part.get_attachment_points():
                                        if pygame.Vector2(ap1).distance_to(ap2) < 10:  # Snap distance
                                            current_component.x += ap2[0] - ap1[0]
                                            current_component.y += ap2[1] - ap1[1]
                                            ship.append(current_component)
                                            components.remove(current_component)
                                            current_component = None
                                            snapped = True
                                            break
                                if snapped:
                                    break
                            if not snapped:
                                current_component = None

            # Move the entire ship if the cabin is being dragged
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if cabin.x <= event.pos[0] <= cabin.x + cabin.width and cabin.y <= event.pos[1] <= cabin.y + cabin.height:
                    dx = event.rel[0]
                    dy = event.rel[1]
                    for part in ship:
                        part.x += dx
                        part.y += dy
