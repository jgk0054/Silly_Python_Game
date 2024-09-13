import pygame
import math
import random
from constants import GREEN, BLUE, TRANSPARENT_BLUE, WHITE

class Planet:
    def __init__(self, x, y, radius, gravity_strength, soi, orbit_radius=0, orbit_speed=0, primary=None, name=""):
        self.x = x
        self.y = y
        self.radius = radius
        self.gravity_strength = gravity_strength
        self.soi = soi
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.primary = primary  # Can be a star, planet, or moon
        self.angle = random.uniform(0, 2 * math.pi)  # Start at a random angle
        self.color = GREEN
        self.name = name if name else random.choice(self.load_planet_names())
        self.irregular_shape = self.create_irregular_shape(radius)

    @staticmethod
    def load_planet_names():
        with open("planet_names.txt", "r") as f:
            return [line.strip() for line in f]

    def draw_orbit(self, screen, camera):
        if not self.primary:
            return
        
        # Orbit parameters
        center_x, center_y = camera.apply(pygame.Vector2(self.primary.x, self.primary.y))
        orbit_radius = int(self.orbit_radius * camera.zoom)
        dash_length = 5
        num_dashes = 100

        for i in range(num_dashes):
            angle_start = i * (2 * math.pi / num_dashes)
            angle_end = (i + 0.5) * (2 * math.pi / num_dashes)

            x_start = center_x + orbit_radius * math.cos(angle_start)
            y_start = center_y + orbit_radius * math.sin(angle_start)

            x_end = center_x + orbit_radius * math.cos(angle_end)
            y_end = center_y + orbit_radius * math.sin(angle_end)

            pygame.draw.aaline(screen, TRANSPARENT_BLUE, (x_start, y_start), (x_end, y_end))

    def create_irregular_shape(self, radius):
        points = []
        for angle in range(0, 360, 10):  # Points every 10 degrees
            angle_rad = math.radians(angle)
            r = radius + random.randint(-10, 10)  # Irregularity in radius
            x = r * math.cos(angle_rad)
            y = r * math.sin(angle_rad)
            points.append((x, y))
        return points

    def is_within_influence(self, px, py):
        # Check if the point is within the radius of the planet's SOI
        dx = self.x - px
        dy = self.y - py
        distance = math.sqrt(dx**2 + dy**2)
        return distance <= self.soi

    def update(self, delta_time):
        if self.primary:
            self.angle += self.orbit_speed * delta_time
            self.x = self.primary.x + self.orbit_radius * math.cos(self.angle)
            self.y = self.primary.y + self.orbit_radius * math.sin(self.angle)

    def rotate_point(self, px, py, angle):
        angle_rad = math.radians(angle)
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)

        # Rotate point around the origin (0, 0)
        x_new = px * cos_theta - py * sin_theta
        y_new = px * sin_theta + py * cos_theta

        return x_new, y_new

    def draw(self, screen, camera):
        self.draw_orbit(screen, camera)  # Draw the orbit first
        rotated_shape = [self.rotate_point(px, py, math.degrees(self.angle)) for px, py in self.irregular_shape]
        transformed_shape = [camera.apply(pygame.Vector2(self.x + px, self.y + py)) for px, py in rotated_shape]
        pygame.draw.polygon(screen, self.color, transformed_shape, 2)

        # Draw the planet's name above the planet
        font = pygame.font.SysFont(None, 24)
        name_surface = font.render(self.name, True, WHITE)
        name_position = camera.apply(pygame.Vector2(self.x, self.y - self.radius - 20))
        screen.blit(name_surface, name_position)
