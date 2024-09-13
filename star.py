from planet import Planet
import pygame
from constants import YELLOW

class Star(Planet):
    def __init__(self, x, y, radius, gravity_strength, soi):
        super().__init__(x, y, radius, gravity_strength, soi)
        self.color = YELLOW  # Override color to yellow

    def draw(self, screen, camera):
        # Draw the star with a size that scales with the camera's zoom level
        screen_x, screen_y = camera.apply(pygame.Vector2(self.x, self.y))
        scaled_radius = int(self.radius * camera.zoom)  # Scale radius by zoom level
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), scaled_radius)
