import pygame
import math
from constants import WHITE, THRUST_POWER, RED, WIDTH, HEIGHT
from ship.ship_saver import load_ship
from ship.cabin import Cabin
from ship.engine import Engine

class Lander:
    def __init__(self, x, y, modules=None):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.angle = 0
        self.thrusting = False
        self.modules = modules if modules else []
        self.ROTATION_SPEED = 90  # Degrees per second
        # Find the cabin and set it as the origin
        self.cabin = next((module for module in self.modules if isinstance(module, Cabin)), None)
        if self.cabin:
            self.set_module_positions_relative_to_cabin()

    def set_module_positions_relative_to_cabin(self):
        cabin_center_x = self.cabin.x + self.cabin.width // 2
        cabin_center_y = self.cabin.y + self.cabin.height // 2

        for module in self.modules:
            module.x -= cabin_center_x
            module.y -= cabin_center_y

        # Set cabin's position as the origin
        self.cabin.x = -self.cabin.width // 2
        self.cabin.y = -self.cabin.height // 2

    def draw(self, screen, camera):
        for module in self.modules:
            self.draw_module(module, screen, camera)

        if self.thrusting:
            self.draw_thrust(screen, camera)

    def draw_module(self, module, screen, camera):
        # Rotate each module around the origin (which is the center of the cabin)
        rotated_corners = []
        for corner in module.get_corners():
            # Rotate each corner around the origin (0, 0)
            rotated_x, rotated_y = self.rotate_point(corner[0], corner[1], self.angle, 0, 0)

            # Translate rotated corner by the lander's position in the world
            world_x = rotated_x + self.x
            world_y = rotated_y + self.y

            # Apply camera transformation
            screen_corners = camera.apply(pygame.Vector2(world_x, world_y))
            rotated_corners.append(screen_corners)

        # Draw the module using the rotated and transformed corners
        module.draw_module(screen, rotated_corners)


    def draw_thrust(self, screen, camera):
        for module in self.modules:
            if isinstance(module, Engine):
                thrust_points = [
                    (module.x , module.y + module.height),
                    (module.x + module.width , module.y + module.height),
                    (module.x + module.width/2, module.y + module.height + 20)
                ]
                rotated_thrust_points = [self.rotate_point(px, py, self.angle, 0, 0) for px, py in thrust_points]
                transformed_thrust_points = [camera.apply(pygame.Vector2(px + self.x, py + self.y)) for px, py in rotated_thrust_points]
                pygame.draw.polygon(screen, RED, transformed_thrust_points)

    def rotate_point(self, px, py, angle, cx, cy):
        angle_rad = math.radians(angle)
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)

        # Translate point to origin (relative to the center point)
        px -= cx
        py -= cy

        # Apply rotation
        x_new = px * cos_theta - py * sin_theta
        y_new = px * sin_theta + py * cos_theta

        # Translate point back
        x = x_new + cx
        y = y_new + cy

        return x, y

    def apply_gravity(self, star, planets, delta_time):
        # Apply gravity from the star
        dx = star.x - self.x
        dy = star.y - self.y
        distance = math.hypot(dx, dy)
        if distance > 0:
            force = star.gravity_strength / (distance ** 2)
            self.vx += (dx / distance) * force * delta_time
            self.vy += (dy / distance) * force * delta_time

        # Apply gravity from planets
        for planet in planets:
            dx = planet.x - self.x
            dy = planet.y - self.y
            distance = math.hypot(dx, dy)
            if distance > 0:
                force = planet.gravity_strength / (distance ** 2)
                self.vx += (dx / distance) * force * delta_time
                self.vy += (dy / distance) * force * delta_time

    def apply_thrust(self, delta_time):
        thrust_x = math.sin(math.radians(self.angle)) * THRUST_POWER * delta_time
        thrust_y = -math.cos(math.radians(self.angle)) * THRUST_POWER * delta_time
        self.vx += thrust_x
        self.vy += thrust_y

    def update(self, delta_time):
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time


    def rotate_left(self, delta_time):
        self.angle += self.ROTATION_SPEED * delta_time

    def rotate_right(self, delta_time):
        self.angle -= self.ROTATION_SPEED * delta_time

    @classmethod
    def from_file(cls, filename):
        modules = load_ship(filename)
        x, y = 0, 25000
        return cls(x, y, modules)
