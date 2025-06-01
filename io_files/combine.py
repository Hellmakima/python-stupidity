import pygame as p
import numpy as np
import math
import random

# Initialize Pygame
p.init()

# Screen setup
WIDTH, HEIGHT = 700, 700
SCREEN = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("3D Cube + Star Field (Persistent Rotation)")
clock = p.time.Clock()

# ===== CUBE SYSTEM =====
cube_size = 100
cube_depth = 500
cube_vertices = np.array([
    [-cube_size, -cube_size, -cube_size], [cube_size, -cube_size, -cube_size],
    [cube_size, cube_size, -cube_size], [-cube_size, cube_size, -cube_size],
    [-cube_size, -cube_size, cube_size], [cube_size, -cube_size, cube_size],
    [cube_size, cube_size, cube_size], [-cube_size, cube_size, cube_size]
], dtype=float)

# Store original vertices for reference
original_vertices = cube_vertices.copy()

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def cube_project(point):
    perspective = cube_depth / (cube_depth - point[2])
    x = int(WIDTH / 2 + point[0] * perspective)
    y = int(HEIGHT / 2 - point[1] * perspective)
    return x, y

def cube_rotate_matrix(axis, angle):
    axis = axis / np.linalg.norm(axis)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x, y, z = axis
    return np.array([
        [cos_a + x*x*(1 - cos_a), x*y*(1 - cos_a) - z*sin_a, x*z*(1 - cos_a) + y*sin_a],
        [y*x*(1 - cos_a) + z*sin_a, cos_a + y*y*(1 - cos_a), y*z*(1 - cos_a) - x*sin_a],
        [z*x*(1 - cos_a) - y*sin_a, z*y*(1 - cos_a) + x*sin_a, cos_a + z*z*(1 - cos_a)]
    ])

# Rotation accumulator
cube_rotation_accum = np.eye(3)

# ===== STAR SYSTEM =====
STAR_CENTER = (WIDTH//2, HEIGHT//2)
star_offset = [0, 0]
stars = []

def star_get_position(star):
    x, y = star    
    x -= star_offset[0]*0.02
    y -= star_offset[1]*0.02
    if not (0 < x < WIDTH and 0 < y < HEIGHT):
        return None
    center = STAR_CENTER[0]+star_offset[0], STAR_CENTER[1]+star_offset[1]
    dx, dy = center[0]-x, center[1]-y
    x -= dx*0.05
    y -= dy*0.05
    return x, y

def make_stars(num):
    return [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(num)]

def star_get_thickness(star):
    x, y = star
    x -= STAR_CENTER[0]+star_offset[0]
    y -= STAR_CENTER[1]+star_offset[1]
    return int(min(3, 1 + (x*x + y*y)**0.5 / 100))

# ===== MAIN LOOP =====
running = True
while running:
    # Event handling
    for event in p.event.get():
        if event.type == p.QUIT or p.key.get_pressed()[p.K_ESCAPE]:
            running = False
    
    # Get mouse movement ONCE per frame
    mouse_rel = p.mouse.get_rel()
    
    # Clear screen
    SCREEN.fill((0, 0, 0))
    
    # ===== STAR SYSTEM UPDATE =====
    star_offset[0] += mouse_rel[0]
    star_offset[1] += mouse_rel[1]
    
    star_offset[0] = max(-WIDTH//2, min(WIDTH//2, star_offset[0]))
    star_offset[1] = max(-HEIGHT//2, min(HEIGHT//2, star_offset[1]))
    
    star_offset[0] *= 0.99
    star_offset[1] *= 0.99
    
    stars.extend(make_stars(10))
    new_stars = []
    for star in stars:
        old_pos = star
        new_pos = star_get_position(star)
        if new_pos is not None:
            new_stars.append(new_pos)
            p.draw.line(SCREEN, (255, 255, 255), old_pos, new_pos, star_get_thickness(star))
    stars = new_stars
    
    # ===== CUBE SYSTEM UPDATE =====
    # Calculate frame rotation
    rot_y = cube_rotate_matrix(np.array([0, 1, 0]), mouse_rel[0] * 0.01)
    rot_x = cube_rotate_matrix(np.array([1, 0, 0]), mouse_rel[1] * 0.01)
    frame_rotation = np.dot(rot_y, rot_x)
    
    # Accumulate rotation
    cube_rotation_accum = np.dot(frame_rotation, cube_rotation_accum)
    
    # Apply accumulated rotation to original vertices
    rotated_vertices = [np.dot(cube_rotation_accum, vertex) for vertex in original_vertices]
    
    # Draw cube
    for edge in cube_edges:
        start = cube_project(rotated_vertices[edge[0]])
        end = cube_project(rotated_vertices[edge[1]])
        p.draw.line(SCREEN, (200, 200, 200), start, end, 2)
    
    p.display.flip()
    clock.tick(60)

p.quit()