import numpy as np
from settings import MOVEMENT_SPEED

class Camera:
    def __init__(self):
        self.pos = np.array([0.0, 0.0, 0.0])
        self.yaw = 0.0
        self.pitch = 0.0
    
    def get_view_matrix(self):
        cos_y, sin_y = np.cos(self.yaw), np.sin(self.yaw)
        cos_p, sin_p = np.cos(self.pitch), np.sin(self.pitch)

        rot_y = np.array([
            [ cos_y, 0, sin_y],
            [     0, 1,     0],
            [-sin_y, 0, cos_y]
        ])
        rot_x = np.array([
            [1,     0,      0],
            [0, cos_p, -sin_p],
            [0, sin_p,  cos_p]
        ])
        return rot_x @ rot_y
    

    def move(self, keys, dt, colliders):
        speed = MOVEMENT_SPEED * dt

        # Camera direction on XZ plane
        forward = np.array([
            -np.sin(self.yaw),
            0,
            np.cos(self.yaw)
        ])

        right = np.array([
            np.cos(self.yaw),
            0,
            np.sin(self.yaw)
        ])

        direction = np.array([0.0, 0.0, 0.0])

        if keys.get("w"):
            direction += forward
        if keys.get("s"):
            direction -= forward
        if keys.get("a"):
            direction -= right
        if keys.get("d"):
            direction += right
        if keys.get("space"):
            direction[1] += 1
        if keys.get("shift"):
            direction[1] -= 1

        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)

        proposed_pos = self.pos + direction * speed
        if not collides(proposed_pos, colliders):
            self.pos[:] = proposed_pos
    
    def rotate(self, dx, dy, sensitivity):
        self.yaw -= dx * sensitivity
        self.pitch -= dy * sensitivity
        self.pitch = max(-np.pi/2, min(np.pi/2, self.pitch))

def collides(pos, colliders, radius=0.8):
    for min_corner, max_corner in colliders:
        expanded_min = min_corner - radius
        expanded_max = max_corner + radius
        if all(expanded_min <= pos) and all(pos <= expanded_max):
            return True
    return False