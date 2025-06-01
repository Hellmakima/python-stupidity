import pygame as p
import random
p.init()
WIDTH, HEIGHT = 500, 500
CENTER = (WIDTH//2, HEIGHT//2)
CENTER_OFFSET = [0, 0]
SCREEN = p.display.set_mode((WIDTH, HEIGHT))
screen = p.Surface((WIDTH, HEIGHT), p.SRCALPHA) 
clock = p.time.Clock()
stars = []

def get_position(star):
    x, y = star    
    x -= CENTER_OFFSET[0]*0.02
    y -= CENTER_OFFSET[1]*0.02
    if not (0 < x < WIDTH and 0 < y < HEIGHT):
        return None
    # push away from CENTER
    center = CENTER[0]+CENTER_OFFSET[0], CENTER[1]+CENTER_OFFSET[1]
    dx, dy = center[0]-x, center[1]-y
    x -= dx*0.05
    y -= dy*0.05
    return x, y

def make_stars(num):
    stars = [(random.randint(0, 500), random.randint(0, 500)) for _ in range(num)]
    return stars

def get_thickness(star):
    x, y = star
    x -= CENTER[0]+CENTER_OFFSET[0]
    y -= CENTER[1]+CENTER_OFFSET[1]
    return int(min(3, 1 + (x*x + y*y)**0.5 / 100))

while True:
    clock.tick(60)
    screen.fill((0, 0, 0, 50))
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            quit()
    keys = p.key.get_pressed()
    offset_change = 10
    if keys[p.K_ESCAPE]:
        p.quit()
        quit()
    # if keys[p.K_LEFT]:
    #     CENTER_OFFSET[0] -= offset_change
    # if keys[p.K_RIGHT]:
    #     CENTER_OFFSET[0] += offset_change
    # if keys[p.K_UP]:
    #     CENTER_OFFSET[1] -= offset_change
    # if keys[p.K_DOWN]:
    #     CENTER_OFFSET[1] += offset_change
    mouse_rel = p.mouse.get_rel()
    CENTER_OFFSET[0] += mouse_rel[0]
    CENTER_OFFSET[1] += mouse_rel[1]

    if CENTER_OFFSET[0] > WIDTH//2:
        CENTER_OFFSET[0] = WIDTH//2
    if CENTER_OFFSET[0] < -WIDTH//2:
        CENTER_OFFSET[0] = -WIDTH//2
    if CENTER_OFFSET[1] > HEIGHT//2:
        CENTER_OFFSET[1] = HEIGHT//2
    if CENTER_OFFSET[1] < -HEIGHT//2:
        CENTER_OFFSET[1] = -HEIGHT//2
    
    CENTER_OFFSET[0] *= 0.99
    CENTER_OFFSET[1] *= 0.99

    stars.extend(make_stars(5))
    new_stars = []
    for star in stars:
        old_pos = star
        star = get_position(star)
        if star is not None:
            new_stars.append(star)
            p.draw.line(screen, (255, 255, 255), old_pos, star, get_thickness(star))
    stars = new_stars
    SCREEN.blit(screen, (0,0))
    p.display.update()
