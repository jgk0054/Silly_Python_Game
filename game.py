import pygame
from planet import Planet
from star import Star
from lander import Lander
from camera import Camera
from utilities import draw_trajectory, draw_ui, polygons_collide
from constants import WIDTH, HEIGHT, BLACK, FPS

def game_loop(screen):
    # Set up your planetary system
    global_primary = Planet(WIDTH // 2, HEIGHT // 2, radius=10000, gravity_strength=1000000000, soi=1000000, orbit_radius=0, orbit_speed=0, primary=None, name="Gas Giant")

    planet1 = Planet(global_primary.x, global_primary.y, radius=1000, gravity_strength=90000000, soi=30000, orbit_radius=25000, orbit_speed=0.002, primary=global_primary)
    planet2 = Planet(global_primary.x, global_primary.y, radius=1000, gravity_strength=90000000, soi=30000, orbit_radius=40000, orbit_speed=0.00015, primary=global_primary)
    planet3 = Planet(global_primary.x, global_primary.y, radius=2000, gravity_strength=90000000, soi=30000, orbit_radius=140000, orbit_speed=0.0001, primary=global_primary)

    moon1 = Planet(planet1.x, planet1.y, 200, 100, 200, orbit_radius=3000, orbit_speed=0.01, primary=planet1)
    moon2 = Planet(planet1.x, planet1.y, 150, 50, 150, orbit_radius=5000, orbit_speed=0.005, primary=planet1)

    planets = [planet1, planet2, planet3, moon1, moon2]

    lander = Lander.from_file("ship.txt")
    camera = Camera(WIDTH, HEIGHT)
    clock = pygame.time.Clock()  # Initialize clock

    running = True
    while running:
        screen.fill(BLACK)
        delta_time = clock.tick(FPS) / 1000.0  # Time since last frame in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    camera.zoom_in()
                elif event.y < 0:
                    camera.zoom_out()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    lander.x, lander.y = WIDTH // 2, HEIGHT // 2 + 15000
                    lander.vx, lander.vy = 0, 0
                    lander.angle = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            lander.rotate_left(delta_time)
        if keys[pygame.K_RIGHT]:
            lander.rotate_right(delta_time)
        if keys[pygame.K_UP]:
            lander.apply_thrust(delta_time)
            lander.thrusting = True
        else:
            lander.thrusting = False

        # Update planets
        for planet in planets:
            planet.update(delta_time)

        # Determine active gravity body
        active_body = global_primary
        for planet in planets:
            if planet.is_within_influence(lander.x, lander.y):
                active_body = planet
                break

        # Apply gravity and update lander
        lander.apply_gravity(global_primary, planets, delta_time)
        lander.update(delta_time)

        # Collision detection
        lander_modules = lander.get_transformed_modules()
        collision_detected = False

        # Include global_primary in collision detection
        all_planets = [global_primary] + planets

        for planet in all_planets:
            planet_shape = planet.get_transformed_shape()
            for module_shape in lander_modules:
                if polygons_collide(module_shape, planet_shape) and lander.isGrounded == False:
                    collision_detected = True
                    print(f"Collision detected between Lander and {planet.name}!")
                    # Handle collision (e.g., stop lander's movement)
                    lander.vx = 0
                    lander.vy = 0
                    lander.isGrounded = True
                    # Optionally, you can add more sophisticated collision response here
                    break  # Exit module loop
            if collision_detected:
                break  # Exit planet loop
            else:
                lander.isGrounded = False

        # Draw everything
        screen.fill(BLACK)
        draw_trajectory(screen, lander, planets, global_primary, camera)
        global_primary.draw(screen, camera)
        for planet in planets:
            planet.draw(screen, camera)

        lander.draw(screen, camera)

        reset_button = draw_ui(screen, lander, active_body, camera, clock)

        camera.update(lander)
        pygame.display.flip()

    pygame.quit()
