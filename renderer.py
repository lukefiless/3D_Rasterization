import pygame
import numpy as np

from utils import (
    project, is_backface, calculate_depth,
    compute_lighting, clip_triangle_near_place
)

from settings import RENDER_DISTANCE
from blocks import BLOCK_TYPES

def draw_triangle(screen, tri, color):
    try:
        points = [project(v) for v in tri]
        if all((x < 0 or x >= screen.get_width() or y < 0 or y >= screen.get_height())for x, y in points):
            return  # completely off-screen
        pygame.draw.polygon(screen, color, points)
    except Exception as e:
        print("Failed to draw triangle:", e)

def draw_scene(screen, camera, scene, colliders):
    view_matrix = camera.get_view_matrix()
    visible_tris = []

    for tri, tag in scene:
        world_tri = np.array(tri)

        camera_space_tri = []
        for v in tri:
            relative = v - camera.pos
            camera_space_tri.append(view_matrix @ relative)

        if is_backface(np.array(camera_space_tri), camera.pos):
            continue

        clipped_tris = clip_triangle_near_place(camera_space_tri)

        for transformed in clipped_tris:
            depth = calculate_depth(world_tri, camera.pos)
            if depth > RENDER_DISTANCE:
                continue

            base_color = BLOCK_TYPES.get(tag, {"color": (255, 0, 255)})["color"]  # magenta for unknown
            shaded_color = compute_lighting(world_tri, base_color, camera.pos, depth, RENDER_DISTANCE)
            visible_tris.append((transformed, shaded_color, depth))
    visible_tris.sort(key=lambda x: x[2], reverse=True)
    for tri, color, _ in visible_tris:
        draw_triangle(screen, tri, color)
