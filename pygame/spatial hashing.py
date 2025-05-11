# inspired by https://github.com/SebLague/Fluid-Sim https://www.youtube.com/watch?v=rSKMYc1CQHE
# spatial hashing is used in particle simulations to reduce number of calculations.

from random import randint
import pygame
import math
from collections import defaultdict
cell_particle_map = defaultdict(list)

# Constants (adjust as needed)
PARTICLE_COUNT = 200
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 100  # Adjust based on your visualization
NUM_CELLS_X = WIDTH // CELL_SIZE
NUM_CELLS_Y = HEIGHT // CELL_SIZE

# Hashing constants (same as in the HLSL code)
# both are primes
HASH_K1 = 15823
HASH_K2 = 9737333

# Offsets (same as in the HLSL code)
OFFSETS_2D = [(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]


def get_cell_2d(position, cell_size):
    # get cell coords from x,y position
    return (int(math.floor(position[0] / cell_size)), int(math.floor(position[1] / cell_size)))


def hash_cell_2d(cell):
    # Make a unique hash for each cell
    cell_x, cell_y = cell
    a = cell_x * HASH_K1
    b = cell_y * HASH_K2
    return a + b


# def key_from_hash(hash_value, table_size=NUM_CELLS_X*NUM_CELLS_Y):
def key_from_hash(hash_value, table_size=100):
    # I dont know the ideal no of buckets.
    # table_size is the number of buckets in the hash table
    return hash_value % table_size


def distance(position1, position2):
    return math.sqrt((position1[0] - position2[0])**2 + (position1[1] - position2[1])**2)


def main():
    print('press <space> to go to next point')
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Example particle positions (replace with your data)
    particle_positions = [(randint(0, WIDTH), randint(0, HEIGHT)) for _ in range(PARTICLE_COUNT)]  # Use WIDTH and HEIGHT

    selected_particle_index = 0  # Index of the particle to highlight

    for position in particle_positions:
        cell = get_cell_2d(position, CELL_SIZE)
        hash_value = hash_cell_2d(cell)
        key = key_from_hash(hash_value)

        if key not in cell_particle_map:
            cell_particle_map[key] = []
        cell_particle_map[key].append(position)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print('selected_particle_index:',selected_particle_index)
                [print(key, cell_particle_map[key]) for key in cell_particle_map]
                print()
                selected_particle_index = (selected_particle_index + 1) % len(particle_positions)

        # Clear screen
        screen.fill((0, 0, 0))

        # Visualization (draw cells and particles)
        selected_position = particle_positions[selected_particle_index]
        selected_cell = get_cell_2d(selected_position, CELL_SIZE)

        pygame.draw.circle(screen, (55, 55, 55, 10), selected_position, CELL_SIZE)


        # Draw grid and highlight only neighboring cells using OFFSETS_2D
        for dx, dy in OFFSETS_2D:
            neighbor_cell = (selected_cell[0] + dx, selected_cell[1] + dy)
            x, y = neighbor_cell
            if 0 <= x < NUM_CELLS_X and 0 <= y < NUM_CELLS_Y:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (255, 0, 0), rect, 2)  # Red outline

                key = key_from_hash(hash_cell_2d(neighbor_cell))
                for particle_pos in cell_particle_map.get(key, []):
                    if distance(particle_pos, selected_position) < CELL_SIZE:
                        pygame.draw.circle(screen, (0, 255, 0), particle_pos, 7, 3)
                    else:
                        pygame.draw.circle(screen, (255, 255, 255), particle_pos, 5, 1)

        # Draw rest of the grid
        for x in range(NUM_CELLS_X):
            for y in range(NUM_CELLS_Y):
                if abs(x - selected_cell[0]) > 1 or abs(y - selected_cell[1]) > 1:
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)

        # Draw all particles
        for particle_pos in particle_positions:
            pygame.draw.circle(screen, (255, 255, 255), particle_pos, 3)  

        # Draw selected particle on top (red)
        pygame.draw.circle(screen, (255, 0, 0), selected_position, 8)  # Larger red circle

        pygame.display.flip()
        # selected_particle_index += 1
        # selected_particle_index %= PARTICLE_COUNT
        clock.tick(20)

    pygame.quit()


if __name__ == "__main__":
    main()