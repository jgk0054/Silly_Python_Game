import pygame
from planet import Planet
from star import Star
from lander import Lander
from camera import Camera
from utilities import draw_trajectory, draw_ui
from constants import WIDTH, HEIGHT, BLACK, FPS

def game_loop(screen):
    # You can now set either a Star or a Planet as the global primary
    global_primary = Planet(WIDTH // 2, HEIGHT // 2, radius=10000, gravity_strength=1000000000, soi=1000000, orbit_radius=0, orbit_speed=0, primary=None, name="Gas Giant")  # Example of a gas giant

    planet1 = Planet(global_primary.x, global_primary.y, radius=1000, gravity_strength=90000000, soi=30000, orbit_radius=25000, orbit_speed=0.02, primary=global_primary)
    planet2 = Planet(global_primary.x, global_primary.y, radius=1000, gravity_strength=90000000, soi=30000, orbit_radius=40000, orbit_speed=0.0015, primary=global_primary)
    planet3 = Planet(global_primary.x, global_primary.y, radius=2000, gravity_strength=90000000, soi=30000, orbit_radius=140000, orbit_speed=0.001, primary=global_primary)

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
                    lander.vx, lander.vy = 0 , 0
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

        # Draw everything
        screen.fill(BLACK)
        draw_trajectory(screen, lander, planets, global_primary, camera)
        global_primary.draw(screen, camera)
        for planet in planets:
            planet.draw(screen, camera)

        lander.draw(screen, camera)

        reset_button = draw_ui(screen, lander, active_body, camera)

        camera.update(lander)
        pygame.display.flip()

    pygame.quit()
