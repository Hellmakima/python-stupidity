import pygame as p
from math import radians, sin, cos
c = p.time.Clock()
h = 200
w = p.display.set_mode((h, h))
n = 5
l = [i/n*200 for i in range(n)]
v = 7
r = 50
while 1:
	c.tick(60)
	w.fill('black')
	for event in p.event.get():
		if event.type == p.QUIT:
			exit()
	for i in range(len(l)):
		l[i] += v + sin(radians(l[i])) * 5
		if (l[i]%(360*3)) // 360 != 1:
			p.draw.circle(w,'white',(h/2 + r * sin(radians(l[i])), h/2 + r * cos(radians(l[i]))), 3)
	p.display.flip()
