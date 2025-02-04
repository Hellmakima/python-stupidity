# inspired by https://github.com/SebLague/Fluid-Sim https://www.youtube.com/watch?v=rSKMYc1CQHE
# spatial hashing is used in particle simulations to reduce number of calculations.

from random import randint
import pygame
import math

# Constants (adjust as needed)
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 100  # Adjust based on your visualization
NUM_CELLS_X = WIDTH // CELL_SIZE
NUM_CELLS_Y = HEIGHT // CELL_SIZE

# Hashing constants (same as in the HLSL code)
HASH_K1 = 15823
HASH_K2 = 9737333

# Offsets (same as in the HLSL code)
OFFSETS_2D = [(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]


def get_cell_2d(position, cell_size):
    return (int(math.floor(position[0] / cell_size)), int(math.floor(position[1] / cell_size)))


def hash_cell_2d(cell):
    cell_x, cell_y = cell
    a = cell_x * HASH_K1
    b = cell_y * HASH_K2
    return a + b


def key_from_hash(hash_value, table_size=100):
    # table_size is the number of buckets in the hash table
    return hash_value % table_size


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Example particle positions (replace with your data)
    particle_positions = [(randint(0, WIDTH), randint(0, HEIGHT)) for _ in range(20)]  # Use WIDTH and HEIGHT

    selected_particle_index = 0  # Index of the particle to highlight

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

        # Spatial Hashing
        cell_particle_map = {}  # Hash table (dictionary)

        for position in particle_positions:
            cell = get_cell_2d(position, CELL_SIZE)
            hash_value = hash_cell_2d(cell)
            key = key_from_hash(hash_value)

            if key not in cell_particle_map:
                cell_particle_map[key] = []
            cell_particle_map[key].append(position)

        # Visualization (draw cells and particles)
        selected_position = particle_positions[selected_particle_index]
        selected_cell = get_cell_2d(selected_position, CELL_SIZE)

        pygame.draw.circle(screen, (55, 55, 55, 10), selected_position, CELL_SIZE)

        for x in range(NUM_CELLS_X):
            for y in range(NUM_CELLS_Y):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell = (x, y)

                # Highlight selected cell and neighbors
                if cell == selected_cell or (cell[0] >= selected_cell[0]-1 and cell[0] <= selected_cell[0]+1 and cell[1] >= selected_cell[1]-1 and cell[1] <= selected_cell[1]+1) :
                    pygame.draw.rect(screen, (255, 0, 0), rect, 2)  # Red outline
                else:
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)  # Draw grid

                hash_value = hash_cell_2d(cell)
                key = key_from_hash(hash_value)

                if key in cell_particle_map:
                    for particle_pos in cell_particle_map[key]:
                        pygame.draw.circle(screen, (255, 255, 255), particle_pos, 5)  # Draw particles

        # Draw selected particle on top (red)
        pygame.draw.circle(screen, (255, 0, 0), selected_position, 8)  # Larger red circle

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()