import pygame
from ship.ship_module import ShipModule

class Radiator(ShipModule):
    def __init__(self, x, y):
        width, height = 100, 20
        attachment_points = [(0, height // 2), (width, height // 2)]  # Left and right center
        super().__init__(x, y, width, height, attachment_points)

    def draw(self, screen, color=(192, 192, 192)):  # Silver-grey color for the radiator
        # Draw the rectangular radiator
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # Draw the attachment points
        for point in self.attachment_points:
            pygame.draw.circle(screen, (0, 255, 0), (self.x + point[0], self.y + point[1]), 5)
