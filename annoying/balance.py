import pygame as p
p.init()
w = p.display.set_mode((200, 100))
s = p.Surface((100, 10))
s2 = p.Surface((200, 20))
clock = p.time.Clock()
mouse_down = 0  # -1 0 1 for left, none and right
percentage = 50


def draw():
    global s, w, percentage
    w.fill('black')
    s.fill('black')
    p.draw.rect(s, "green", (0, 0, percentage, 10))
    p.draw.rect(s, "white", (0, 0, 100, 10), 2)
    s2.blit(s, (50, 5))
    temp = p.transform.rotate(s2, 10*mouse_down)
    a, b = temp.get_size()
    a -= 200
    b -= 200
    w.blit(temp, (-a/2, -b/2 - 50))
    p.display.flip()


vel = 0

while True:
    clock.tick(20)
    for event in p.event.get():
        if event.type == p.KEYDOWN or event.type == p.QUIT:
            exit()
        if event.type == p.MOUSEBUTTONDOWN:
            pos = p.mouse.get_pos()
            if pos[0] > 100:
                mouse_down = -1
            else:
                mouse_down = 1
        if event.type == p.MOUSEBUTTONUP:
            mouse_down = 0
    vel += mouse_down
    vel = max(-10, min(10, vel))
    vel *= 0.8
    percentage -= vel
    percentage = max(0, min(100, percentage))
    draw()
