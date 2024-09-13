import pygame
from ship.ship_module import ShipModule

class FuelTank(ShipModule):
    def __init__(self, x, y):
        width, height = 40, 80
        attachment_points = [(width // 2, 0), (width // 2, height)]  # Top and bottom center
        super().__init__(x, y, width, height, attachment_points)

    def get_corners(self):
        return [
            (self.x, self.y),  # Top-left
            (self.x + self.width, self.y),  # Top-right
            (self.x + self.width, self.y + self.height),  # Bottom-right
            (self.x, self.y + self.height),  # Bottom-left
        ]

    def draw_module(self, screen, corners):
        pygame.draw.polygon(screen, (0, 0, 255), corners)
