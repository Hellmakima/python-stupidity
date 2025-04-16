import pygame as p
p.init()
w = p.display.set_mode((300, 300))
clock = p.time.Clock()
percentage = 50

acc = 1
move = 0
pumping = False
hh = 180
while True:
    clock.tick(20)
    w.fill('black')
    for event in p.event.get():
        if event.type == p.KEYDOWN or event.type == p.QUIT:
            exit()
        if event.type == p.MOUSEBUTTONDOWN:
            pumping = True
        if event.type == p.MOUSEBUTTONUP:
            pumping = False
    if pumping:
        move = p.mouse.get_rel()[1]
        hh = p.mouse.get_pos()[1]
    percentage += abs(move) * .1
    percentage -= acc
    percentage = max(0, min(100, percentage))
    p.draw.line(w, 'white', (125, hh), (175, hh))
    p.draw.line(w, 'white', (150, hh), (150, 200))
    p.draw.rect(w, 'green', (125, 300-percentage, 50, percentage))
    p.draw.rect(w, 'white', (125, 200, 50, 100), 2)
    p.display.flip()
