import pygame, random
from pygame.math import Vector2

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle collision in space")
font = pygame.font.Font(None, 36)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
G = 1.0          # Gravitational constant
DT = 0.1         # Time step
DAMPING = 0.9    # Energy loss on collisions

class Particle:
    def __init__(self, pos, vel, radius, mass, color):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.next_vel = Vector2(vel)
        self.next_pos = Vector2(pos)
        self.radius = radius
        self.mass = mass
        self.color = color
        self.collision_offset = Vector2(0, 0)
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        
    def reset_next_state(self):
        self.next_vel = self.vel.copy()
        self.collision_offset = Vector2(0, 0)
        self.next_pos = self.pos.copy()
        
    def apply_next_state(self):
        self.vel = self.next_vel.copy()
        self.pos = self.next_pos.copy()

def process_interaction(p, q):
    diff = q.pos - p.pos
    dist = diff.length() if diff.length() != 0 else 0.0001  # avoid division by zero
    # Gravity applies only if within max influence radius (10 * max radius)
    influence_threshold = 10 * max(p.radius, q.radius)
    if dist < influence_threshold:
        norm = diff.normalize()
        p.next_vel += norm * (G * q.mass / (dist**2)) * DT
        q.next_vel -= norm * (G * p.mass / (dist**2)) * DT
    # Collision resolution if overlapping
    min_dist = p.radius + q.radius
    if dist < min_dist:
        norm = diff.normalize()
        overlap = min_dist - dist
        p.collision_offset -= norm * (overlap / 2)
        q.collision_offset += norm * (overlap / 2)
        relative_vel = p.next_vel - q.next_vel
        impulse = 2 * relative_vel.dot(norm) / (p.mass + q.mass)
        p.next_vel -= impulse * q.mass * norm
        q.next_vel += impulse * p.mass * norm
        p.next_vel *= DAMPING
        q.next_vel *= DAMPING

def apply_interactions(particles):
    cell_size = 200  # Spatial partitioning cell size – a little grid magic!
    grid = {}
    for p in particles:
        cell = (int(p.pos.x // cell_size), int(p.pos.y // cell_size))
        grid.setdefault(cell, []).append(p)

    for cell, plist in grid.items():
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor = (cell[0] + dx, cell[1] + dy)
                if neighbor in grid:
                    for p in plist:
                        for q in grid[neighbor]:
                            if p is q:
                                continue
                            # Avoid double-processing: in same cell, process only if id(p) < id(q); for different cells, process if neighbor > cell lexicographically
                            if (neighbor == cell and id(p) < id(q)) or (neighbor > cell):
                                process_interaction(p, q)

def main():
    particles = [Particle(
        pos=(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)),
        vel=(random.uniform(-2, 2), random.uniform(-2, 2)),
        radius=random.randint(10, 20),
        mass=(random.randint(1, 5))**2,  # mass ∝ area
        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    ) for _ in range(100)]
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # Reset next state for all particles
        for p in particles:
            p.reset_next_state()
            
        apply_interactions(particles)
        
        # Update tentative positions with collision offsets & wall collisions
        for p in particles:
            p.next_pos = p.pos + p.next_vel * DT + p.collision_offset
            if p.next_pos.x - p.radius < 0:
                p.next_vel.x *= -1
                p.next_pos.x = p.radius
            elif p.next_pos.x + p.radius > WIDTH:
                p.next_vel.x *= -1
                p.next_pos.x = WIDTH - p.radius
            if p.next_pos.y - p.radius < 0:
                p.next_vel.y *= -1
                p.next_pos.y = p.radius
            elif p.next_pos.y + p.radius > HEIGHT:
                p.next_vel.y *= -1
                p.next_pos.y = HEIGHT - p.radius
            p.apply_next_state()
            
        # Rendering time!
        screen.fill(BLACK)
        for p in particles:
            p.draw(screen)
        fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True, WHITE)
        screen.blit(fps_text, (10, 10))
        pygame.display.flip()
        clock.tick(1600)
        
    pygame.quit()

if __name__ == "__main__":
    main()
