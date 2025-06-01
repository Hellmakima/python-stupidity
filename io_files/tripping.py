import pygame as p
import random
import math
p.init()

WIDTH, HEIGHT = 500, 500
CENTER = (WIDTH // 2, HEIGHT // 2)
screen = p.display.set_mode((WIDTH, HEIGHT))
clock = p.time.Clock()
stars = []
player_pos = [WIDTH // 2, HEIGHT // 2]
player_vel = [0, 0]
acceleration = 0.2
max_speed = 10

def make_star():
    # Create stars at edges (better for "warp speed" effect)
    side = random.choice(["top", "right", "bottom", "left"])
    if side == "top":
        return (random.randint(0, WIDTH)), 0
    elif side == "right":
        return WIDTH, random.randint(0, HEIGHT)
    elif side == "bottom":
        return (random.randint(0, WIDTH), HEIGHT)
    else:  # left
        return 0, random.randint(0, HEIGHT)

for _ in range(100):
    stars.append(make_star())

running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time for smooth movement

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    # Handle key presses (WASD or Arrow Keys)
    keys = p.key.get_pressed()
    if keys[p.K_LEFT] or keys[p.K_a]:
        player_vel[0] -= acceleration
    if keys[p.K_RIGHT] or keys[p.K_d]:
        player_vel[0] += acceleration
    if keys[p.K_UP] or keys[p.K_w]:
        player_vel[1] -= acceleration
    if keys[p.K_DOWN] or keys[p.K_s]:
        player_vel[1] += acceleration

    # Apply friction (gradual slowdown)
    player_vel[0] *= 0.95
    player_vel[1] *= 0.95

    # Limit speed
    speed = math.sqrt(player_vel[0]**2 + player_vel[1]**2)
    if speed > max_speed:
        player_vel[0] = player_vel[0] / speed * max_speed
        player_vel[1] = player_vel[1] / speed * max_speed

    # Move player (wrap around screen edges)
    player_pos[0] = (player_pos[0] + player_vel[0]) % WIDTH
    player_pos[1] = (player_pos[1] + player_vel[1]) % HEIGHT

    # Update stars (move opposite to player velocity)
    screen.fill('black')
    new_stars = []
    for x, y in stars:
        # Stars move away from center (scaled by player speed)
        dx = x - player_pos[0]
        dy = y - player_pos[1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 5:  # Remove stars too close to player
            continue

        # Streak effect: stars further away move faster
        x -= player_vel[0] * (1 + dist / 100)
        y -= player_vel[1] * (1 + dist / 100)

        # Wrap stars around screen
        x = x % WIDTH
        y = y % HEIGHT

        # Draw star (size scales with speed)
        size = min(3, 1 + speed / 3)
        p.draw.circle(screen, (255, 255, 255), (int(x), int(y)), int(size))
        new_stars.append((x, y))

    stars = new_stars

    # Add new stars if needed
    while len(stars) < 100:
        stars.append(make_star())

    p.display.update()

p.quit()