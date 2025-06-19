from settings import (
    WIDTH, HEIGHT, MOUSE_SENSITIVITY, SKY_COLOR
)

from renderer import draw_scene
from camera import Camera
from world import World

from blocks import make_cube, cube_aabb, BLOCK_TYPES, BLOCK_NAME_TO_ID

import numpy as np
import pygame

# === SETUP ===
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Consolas", 18)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clone")
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
clock = pygame.time.Clock()


# === GAME STATE ===
paused = False
running = True
camera = Camera()
camera.pos = np.array([0.0, 5.0, 0.0])  # or higher if your terrain is tall
world = World()
world.generate_flat(width=5, depth=5, height=2)
scene = world.get_scene()
colliders = world.get_colliders()

world.add_block((0, 2, 0), BLOCK_NAME_TO_ID["stone"])
world.add_block((1, 2, 0), BLOCK_NAME_TO_ID["stone"])
world.add_block((0, 2, 1), BLOCK_NAME_TO_ID["stone"])


# === MAIN LOOP ===
while running:
    dt = clock.tick(60) / 1000
    screen.fill(SKY_COLOR)

    # get mouse movement
    keys = pygame.key.get_pressed()

    if not paused:
        keys_pressed = {
            "w": keys[pygame.K_w],
            "s": keys[pygame.K_s],
            "a": keys[pygame.K_a],
            "d": keys[pygame.K_d],
            "space": keys[pygame.K_SPACE],
            "shift": keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT],
        }
        camera.move(keys_pressed, dt, colliders)

        dx, dy = pygame.mouse.get_rel()
        camera.rotate(dx, dy, MOUSE_SENSITIVITY)
    
    draw_scene(screen, camera, scene, colliders)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                pygame.event.set_grab(not paused)
                pygame.mouse.set_visible(paused)



    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
    screen.blit(fps_text, (WIDTH - 100, 10))  # Top-right corner
    pygame.display.flip()

pygame.quit()