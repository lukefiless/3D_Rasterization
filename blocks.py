import numpy as np

BLOCK_AIR = 0
BLOCK_GRASS = 1
BLOCK_DIRT = 2
BLOCK_STONE = 3

BLOCK_NAME_TO_ID = {
    "grass": BLOCK_GRASS,
    "dirt": BLOCK_DIRT,
    "stone": BLOCK_STONE
}

BLOCK_TYPES = {
    BLOCK_GRASS: {"name": "Grass", "color": (34, 139, 34)},
    BLOCK_DIRT: {"name": "Dirt", "color": (139, 69, 19)},
    BLOCK_STONE: {"name": "Stone", "color": (128, 128, 128)},
}

def make_cube(center, size=2):
    x,y,z = center
    s = size / 2
    return [
        # Front face
        [[x-s, y-s, z-s], [x+s, y-s, z-s], [x+s, y+s, z-s]],
        [[x-s, y-s, z-s], [x+s, y+s, z-s], [x-s, y+s, z-s]],
        # Back face
        [[x+s, y-s, z+s], [x-s, y-s, z+s], [x-s, y+s, z+s]],
        [[x+s, y-s, z+s], [x-s, y+s, z+s], [x+s, y+s, z+s]],
        # Left face
        [[x-s, y-s, z+s], [x-s, y-s, z-s], [x-s, y+s, z-s]],
        [[x-s, y-s, z+s], [x-s, y+s, z-s], [x-s, y+s, z+s]],
        # Right face
        [[x+s, y-s, z-s], [x+s, y-s, z+s], [x+s, y+s, z+s]],
        [[x+s, y-s, z-s], [x+s, y+s, z+s], [x+s, y+s, z-s]],
        # Top face
        [[x-s, y+s, z-s], [x+s, y+s, z-s], [x+s, y+s, z+s]],
        [[x-s, y+s, z-s], [x+s, y+s, z+s], [x-s, y+s, z+s]],
        # Bottom face
        [[x-s, y-s, z+s], [x+s, y-s, z+s], [x+s, y-s, z-s]],
        [[x-s, y-s, z+s], [x+s, y-s, z-s], [x-s, y-s, z-s]],
    ]

def cube_aabb(center, size):
    x, y, z = center
    s = size / 2
    return np.array([x - s, y - s, z - s]), np.array([x + s, y + s, z + s])

def get_cube_face(center, face_index, size=1):
    x, y, z = center
    s = size / 2

    faces = [
        # 0: Right
        [[x+s, y-s, z-s], [x+s, y-s, z+s], [x+s, y+s, z+s]],
        [[x+s, y-s, z-s], [x+s, y+s, z+s], [x+s, y+s, z-s]],

        # 1: Left
        [[x-s, y-s, z+s], [x-s, y-s, z-s], [x-s, y+s, z-s]],
        [[x-s, y-s, z+s], [x-s, y+s, z-s], [x-s, y+s, z+s]],

        # 2: Top
        [[x-s, y+s, z-s], [x+s, y+s, z-s], [x+s, y+s, z+s]],
        [[x-s, y+s, z-s], [x+s, y+s, z+s], [x-s, y+s, z+s]],

        # 3: Bottom
        [[x-s, y-s, z+s], [x+s, y-s, z+s], [x+s, y-s, z-s]],
        [[x-s, y-s, z+s], [x+s, y-s, z-s], [x-s, y-s, z-s]],

        # 4: Front
        [[x-s, y-s, z-s], [x+s, y-s, z-s], [x+s, y+s, z-s]],
        [[x-s, y-s, z-s], [x+s, y+s, z-s], [x-s, y+s, z-s]],

        # 5: Back
        [[x+s, y-s, z+s], [x-s, y-s, z+s], [x-s, y+s, z+s]],
        [[x+s, y-s, z+s], [x-s, y+s, z+s], [x+s, y+s, z+s]],
    ]
    return faces[face_index * 2 : face_index * 2 + 2]