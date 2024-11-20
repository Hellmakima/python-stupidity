import pygame as p
from random import randint
p.init()


# states: mine(1)/no(0) & number(0-8) & state(close(0), marked(1), open(2))

W, H = 600,400
tile = 20
font = p.font.SysFont('Arial', int(tile*0.8))

grid_w, grid_h = W//tile, H//tile

w = p.display.set_mode((W, H))

# make grid
a = [[[0]*3 for i in range(grid_w)] for _ in range(grid_h)]

def fill_mines(mines=(grid_h*grid_w)//6, pos=(grid_h//2, grid_w//2)):
	i,j = pos
	void = [(i-1, j-1), (i-1, j), (i-1, j+1),
			(i, j-1), (i,j), (i, j+1),
			(i+1, j-1), (i+1, j), (i+1, j+1)]
	while mines:
		x, y = randint(0,grid_h-1), randint(0,grid_w-1)
		if a[x][y][0] == 1 or (x,y) in void:
			continue
		a[x][y][0] = 1
		mines -= 1

def fill_neighbors(a):
	for i in range(grid_h):
		for j in range(grid_w):
			if a[i][j][0] == 1:
				# mine so doesn't matter
				continue
			count = 0
			neighbors = [
				(i-1, j-1), (i-1, j), (i-1, j+1),
				(i, j-1), (i, j+1),
				(i+1, j-1), (i+1, j), (i+1, j+1)
			]
			for x,y in neighbors:
				if -1<x<grid_h and -1<y<grid_w and a[x][y][0] == 1:
					count += 1
			a[i][j][1] = count


def mark(x, y):
	def open(x, y):
		if a[x][y][2] == 2: return
		a[x][y][2] = 2
		if a[x][y][1] != 0: return
		neighbors = [
				(x-1, y-1), (x-1, y), (x-1, y+1),
				(x, y-1), (x, y+1),
				(x+1, y-1), (x+1, y), (x+1, y+1)
			]
		for i,j in neighbors:
			if -1<i<grid_h and -1<j<grid_w:
				open(i,j)
	if a[x][y][0] == 1:
		print('failed')
		exit()
	if a[x][y][1] == 0:
		open(x,y)
	a[x][y][2] = 2


def draw():
	w.fill((70,70,70))
	for i in range(grid_h):
		for j in range(grid_w):
			# p.draw.rect(w, (100,100,100) if a[i][j][2] == 0 else (70,70,70),(j*tile,i*tile,tile,tile))
			if a[i][j][2] == 0:
				p.draw.rect(w, (100,100,100),(j*tile,i*tile,tile,tile))
			elif a[i][j][2] == 1:
				p.draw.rect(w, (200,30,30),(j*tile,i*tile,tile,tile))
			else:
				text = font.render(str(a[i][j][1]) if a[i][j][1] != 0 else '', True, (200,0,0))
				w.blit(text, (j*tile,i*tile))
	# draw grid
	for i in range(1,grid_h):
		p.draw.line(w, 'black', (0, i*tile), (W, i*tile))
	for i in range(1,grid_w):
		p.draw.line(w, 'black', (i*tile, 0), (i*tile, H))
	p.display.flip()


def first_click():
	while True:
		for event in p.event.get():
			if event.type == p.QUIT or event.type == p.KEYDOWN:
				exit()
			if event.type == p.MOUSEBUTTONDOWN:
				loc = p.mouse.get_pos()
				y = loc[0]//tile
				x = loc[1]//tile
				return (x, y)

def main():
	draw()
	pos = first_click()
	fill_mines(pos=pos)
	fill_neighbors(a)
	[print([ii[0] for ii in i]) for i in a]
	mark(*pos)
	draw()
	running = True
	while running:
		for event in p.event.get():
			if event.type == p.QUIT or event.type == p.KEYDOWN:
				running = False
			if event.type == p.MOUSEBUTTONDOWN:
				loc = p.mouse.get_pos()
				y = loc[0]//tile
				x = loc[1]//tile
				# a[x][y][2] = 2
				# print(x,y)
				mark(x, y)
				draw()

if __name__ == '__main__':
	main()