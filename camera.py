import pygame

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.width = width
        self.height = height

    def apply(self, obj):
        return (obj.x - self.x) * self.zoom + self.width // 2, (obj.y - self.y) * self.zoom + self.height // 2

    def update(self, target):
        self.x = target.x
        self.y = target.y

    def zoom_in(self):
        self.zoom *= 1.1

    def zoom_out(self):
        self.zoom *= 0.9
        
    def clone(self):
        new_camera = Camera(self.width, self.height)
        new_camera.x = self.x
        new_camera.y = self.y
        new_camera.zoom = self.zoom
        return new_camera