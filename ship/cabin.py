import pygame
from ship.ship_module import ShipModule

class Cabin(ShipModule):
    def __init__(self, x, y):
        width, height = 80, 100
        attachment_points = [(width // 2, 0), (width // 2, height), (0, height // 2), (width, height // 2)]  # Center on all sides
        super().__init__(x, y, width, height, attachment_points)

    def get_corners(self):
        # Returns the four corners of the cabin relative to its own position
        return [
            (self.x, self.y),  # Top-left
            (self.x + self.width, self.y),  # Top-right
            (self.x + self.width, self.y + self.height),  # Bottom-right
            (self.x, self.y + self.height),  # Bottom-left
        ]

    def draw_module(self, screen, corners):
        pygame.draw.polygon(screen, (255, 255, 255), corners)
