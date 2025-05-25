import pygame
import sys
import time

pygame.init()
WIDTH, HEIGHT = 800, 200
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typewriter Name Animation")

# Colors and fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WHITE = (0, 0, 0)
BLACK = (255, 255, 255)
FONT = pygame.font.SysFont("Courier New", 48)

frames = [
    "", "", "S", "Su", "Suf", "Suff", "Suffi", "Suffiy", "Suffiya", "Suffiyan", 
    "Suffiya", "Suffiy", "Suffi", "Suff", "Suf", "Sufi", "Sufiy", "Sufiya", "Sufiyan", 
    "Sufiyan ", "Sufiyan A", "Sufiyan At", "Sufiyan Att", "Sufiyan Atta", "Sufiyan Attar", 
    "Sufiyan Attar", "Sufiyan Attar", "Sufiyan Attar", 
    "Sufiyan Att", "Sufiyan A", "Sufiyan", "Sufiy", "Su", "S", ""
]

def draw_text(text):
    WIN.fill(WHITE)
    rendered = FONT.render(text + "|", True, BLACK)
    WIN.blit(rendered, (50, 80))
    pygame.display.update()

WIN.fill(WHITE)
pygame.display.update()
time.sleep(4)
for frame in frames:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    draw_text(frame)
    time.sleep(0.2)
time.sleep(2)
