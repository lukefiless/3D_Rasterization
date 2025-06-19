from blocks import make_cube, cube_aabb, get_cube_face, BLOCK_NAME_TO_ID
from utils import fix_winding

class World:
    def __init__(self):
        self.blocks = {}
        self.colliders = []
        self.scene = []
    
    def add_block(self, pos, block_type):
        x,y,z = pos
        neighbors = [
            (x+1, y, z), (x-1, y, z),
            (x, y+1, z), (x, y-1, z),
            (x, y, z+1), (z, y, z-1)
        ]

        for i, neighbor in enumerate(neighbors):
            if neighbor in self.blocks:
                continue
            face_tris = get_cube_face((x, y, z), i)
            self.scene += [(fix_winding(tri), block_type) for tri in face_tris]

        self.blocks[pos] = block_type
        self.colliders.append(cube_aabb((x,y,z),1))

    def generate_flat(self, width=10, depth=10, height=1):
        for x in range(-width, width):
            for z in range(-depth, depth):
                for y in range(height):
                    block_type = BLOCK_NAME_TO_ID["grass"] if y == height - 1 else BLOCK_NAME_TO_ID["dirt"]
                    self.add_block((x,y,z), block_type)

    def get_scene(self):
        return self.scene
    
    def get_colliders(self):
        return self.colliders