import pygame
import math

class ShipModule:
    def __init__(self, x, y, width, height, attachment_points=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.attachment_points = attachment_points if attachment_points else []

    def draw(self, screen, camera, lander_x, lander_y, lander_angle, scale, show_snap_points=True):
        rotated_x, rotated_y = self.rotate_point(self.x, self.y, lander_angle, 0, 0)
        world_x, world_y = rotated_x + lander_x, rotated_y + lander_y

        if camera:
            screen_x, screen_y = camera.apply(pygame.Vector2(world_x, world_y))
        else:
            screen_x, screen_y = world_x, world_y

        corners = self.get_corners()
        rotated_corners = [self.rotate_point(corner[0], corner[1], lander_angle, 0, 0) for corner in corners]
        world_corners = [(x + lander_x, y + lander_y) for x, y in rotated_corners]
        screen_corners = [camera.apply(pygame.Vector2(x, y)) if camera else (x, y) for x, y in world_corners]

        self.draw_module(screen, screen_corners)

        if show_snap_points:
            for point in self.attachment_points:
                attachment_x = screen_x + int(point[0] * scale)
                attachment_y = screen_y + int(point[1] * scale)
                pygame.draw.circle(screen, (0, 255, 0), (attachment_x, attachment_y), max(1, int(5 * scale)))

    def draw_module(self, screen, corners):
        raise NotImplementedError("Subclasses should implement this method")

    def get_attachment_points(self):
        return [(self.x + point[0], self.y + point[1]) for point in self.attachment_points]

    def rotate_point(self, px, py, angle, cx, cy):
        angle_rad = math.radians(angle)
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)

        px -= cx
        py -= cy

        x_new = px * cos_theta - py * sin_theta
        y_new = px * sin_theta + py * cos_theta

        x = x_new + cx
        y = y_new + cy

        return x, y
