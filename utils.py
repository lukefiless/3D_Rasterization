import numpy as np
from settings import WIDTH, HEIGHT, FOV, LIGHT_POS, SKY_COLOR

def project(v):
    fov = 90
    x, y, z = v
    scale = WIDTH / (2 * np.tan(np.radians(fov) / 2))

    if z == 0: z = 0.0001

    x_proj = int(WIDTH / 2 + x * scale / z)
    y_proj = int(HEIGHT / 2 - y * scale / z)
    return (x_proj, y_proj)

def fix_winding(tri):
    return [tri[0], tri[2], tri[1]]  # reverse second and third to make CCW

def is_backface(tri, camera_pos):
    a, b, c = tri
    ab = b - a
    ac = c - a
    normal = np.cross(ab, ac)

    view_dir = a - camera_pos # vector from camera to tri
    return np.dot(normal, view_dir) >= 0

def calculate_depth(tri, camera_pos):
    # calc average depth(z)
    center = np.mean(tri, axis=0)
    return np.linalg.norm(center - camera_pos)


def compute_lighting(tri, base_color, camera_pos, distance, fog_distance):
    a, b, c = tri
    ab = b - a
    ac = c - a
    normal = np.cross(ab, ac)
    normal = normal / np.linalg.norm(normal)

    center = (a + b + c) / 3
    light_dir = LIGHT_POS - center
    light_dir = light_dir / np.linalg.norm(light_dir)

    # Slightly soften the angle difference to smooth harsh contrast
    diff_strength = max(0.0, np.dot(normal, light_dir)) ** 0.8  # soften sharp falloff

    ambient_strength = 0.5
    ambient = ambient_strength * np.array(base_color)
    diffuse = diff_strength * np.array(base_color)

    # Optional: soften or skip specular
    view_dir = camera_pos - center
    view_dir = view_dir / np.linalg.norm(view_dir)
    reflect_dir = 2 * np.dot(light_dir, normal) * normal - light_dir
    spec_strength = max(0.0, np.dot(view_dir, reflect_dir)) ** 8  # reduce exponent
    specular = spec_strength * np.array([255, 255, 255]) * 0.2    # reduce glare

    result = ambient + (1 - ambient_strength) * diffuse + specular

    # Fog
    fog_color = np.array(SKY_COLOR)
    fog_amount = min(1.0, distance / fog_distance)
    result = result * (1 - fog_amount) + fog_color * fog_amount

    return tuple(min(255, int(c)) for c in result)


def clip_triangle_near_place(tri, near=0.01):
    inside = []
    outside = []

    for v in tri:
        if v[2] >= near:
            inside.append(v)
        else:
            outside.append(v)

    if len(inside) == 0:
        return [] # fully clipped

    if len(inside) == 3:
        return[tri] # fully visible
    
    def interpolate(v1, v2):
        t = (near - v1[2]) / (v2[2] - v1[2])
        return v1 + t * (v2 - v1)

    if len(inside) == 1:
        a = inside[0]
        b = interpolate(a, outside[0])
        c = interpolate(a, outside[1])
        return [[a, b, c]]
    elif len(inside) == 2:
        a, b = inside
        c = interpolate(a, outside[0])
        d = interpolate(b, outside[0])
        return [[a, b, c], [b, d, c]]
