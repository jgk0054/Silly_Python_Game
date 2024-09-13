import pygame
from lander import Lander
from planet import Planet
from star import Star
import math
# Constants
WIDTH, HEIGHT = 1000, 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
FPS = 30

def draw_trajectory(screen, lander, planets, star, camera):
    # Copy the lander's state
    temp_lander = Lander(lander.x, lander.y, modules=lander.modules)
    temp_lander.vx, temp_lander.vy = lander.vx, lander.vy
    temp_lander.angle = lander.angle
    temp_lander.thrusting = False  # Assuming no thrust during prediction

    # Create a copy of planets but do not update their positions during simulation
    temp_planets = [
        Planet(
            p.x, p.y, p.radius, p.gravity_strength, p.soi,
            orbit_radius=p.orbit_radius, orbit_speed=p.orbit_speed, primary=p.primary, name=p.name
        )
        for p in planets
    ]
    # Planets remain stationary during trajectory prediction

    num_steps = 500  # Adjust as needed
    delta_time = 1 / FPS  # Assuming FPS is defined and consistent

    trajectory_points = []
    for _ in range(num_steps):
        # Apply gravity
        temp_lander.apply_gravity(star, temp_planets, delta_time)
        # Update lander position
        temp_lander.update(delta_time)

        # Transform position to screen coordinates
        projected_point = camera.apply(pygame.Vector2(temp_lander.x, temp_lander.y))
        trajectory_points.append((int(projected_point[0]), int(projected_point[1])))

    # Draw the trajectory
    if len(trajectory_points) > 1:
        pygame.draw.lines(screen, (255, 255, 255, 128), False, trajectory_points, 2)

def calculate_orbital_speed(lander, body):
    dx = lander.x - body.x
    dy = lander.y - body.y
    relative_velocity = math.sqrt(lander.vx**2 + lander.vy**2)

    # Handle the star differently (no orbit_radius for the star)
    if isinstance(body, Star):
        # Orbital speed relative to the star is just the velocity in the star's gravitational field
        return relative_velocity
    
    # For planets, calculate based on the orbit radius
    if body.orbit_radius == 0 or relative_velocity == 0:
        return 0.0

    return relative_velocity - math.sqrt(dx**2 + dy**2) / body.orbit_radius

def draw_ui(screen, lander, active_body, camera):
    font = pygame.font.SysFont(None, 24)  # Smaller font size
    body_name = "Star"
    
    # Display orbital speed
    if isinstance(active_body, Planet):
        body_name = "Planet"

    orbital_speed = calculate_orbital_speed(lander, active_body)
    speed_text = font.render(f"Orbital Speed ({body_name}): {orbital_speed:.2f}", True, WHITE)
    screen.blit(speed_text, (WIDTH - 300, 10))

    # Draw compass
    compass_center = (WIDTH - 50, HEIGHT - 50)
    pygame.draw.circle(screen, WHITE, compass_center, 40, 2)
    angle_rad = math.radians(lander.angle)
    compass_x = compass_center[0] + 30 * math.sin(angle_rad)
    compass_y = compass_center[1] - 30 * math.cos(angle_rad)
    pygame.draw.line(screen, RED, compass_center, (compass_x, compass_y), 4)

    # Draw reset button
    reset_button = pygame.Rect(10, 10, 100, 50)
    pygame.draw.rect(screen, RED, reset_button)
    reset_text = font.render("RESET", True, WHITE)
    screen.blit(reset_text, (20, 20))

    return reset_button


