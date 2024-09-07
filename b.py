import pygame as p
import sys
import random
import math

# Initialize pygame
p.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CAR_RADIUS = 10  # Radius for the car circles
ROAD_WIDTH = 30
FPS = 30  # Increase FPS for smoother animation
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)]  # Define 4 colors
GRAY = (128, 128, 128)

# Create the screen
screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption('Car Simulation')
clock = p.time.Clock()

class Junction():
    def __init__(self):
        self.road_list = []
    def set_road_list(self, road_list, pos):
        self.road_list = road_list
        self.current_side = random.randint(0, len(road_list) - 1)
        self.pos = pos
    def draw(self):
        p.draw.line(screen, 'green', self.pos, self.road_list[self.current_side].end, 3)

class Road():
    def __init__(self, start, end, junction_start, junction_end):
        # single lane
        self.length = max(abs(start[0] - end[0]), abs(start[1] - end[1])) // CAR_RADIUS
        self.start = start  # (x,y)
        self.end = end  # (dx,dy)
        self.left_lane = [None] * self.length
        self.right_lane = [None] * self.length
        self.populate_lanes()
        self.junction_start = junction_start
        self.junction_end = junction_end

    def populate_lanes(self):
        for i in range(self.length):
            # Randomly decide if there is a car in the lane
            if random.choice([True, False]):  # Randomly decide if a car is present
                color_index = random.randint(0, len(COLORS) - 1)  # Pick a random color index
                self.left_lane[i] = (i * CAR_RADIUS, color_index)  # Store position and color index
            if random.choice([True, False]):  # Randomly decide if a car is present
                color_index = random.randint(0, len(COLORS) - 1)  # Pick a random color index
                self.right_lane[i] = (i * CAR_RADIUS, color_index)  # Store position and color index

    def update(self):
        for i in range(1, len(self.left_lane)):
            if self.junction_start is None:
                self.left_lane[0] = None
                if self.right_lane[0] == None and True if random.choices([i for i in '0'*100 +'1']) == ['1'] else False:
                    self.right_lane[0] = (0, random.randint(0, len(COLORS) - 1))
            elif self.left_lane[0] is not None:
                junction = self.junction_start
                if junction.road_list[junction.current_side] == self:
                    turn_to = random.randint(0, len(junction.road_list) - 1)
                    junction.road_list[turn_to].left_lane[0] = self.left_lane[0]
                    self.left_lane[0] = None
            if self.left_lane[i] is not None and self.left_lane[i - 1] is None:
                self.left_lane[i - 1] = self.left_lane[i]
                self.left_lane[i] = None
        for i in range(len(self.right_lane) - 2, -1, -1):
            if self.junction_end is None:
                self.right_lane[-1] = None
            elif self.right_lane[-1] is not None:
                junction = self.junction_end
                if junction.road_list[junction.current_side] == self:
                    turn_to = random.randint(0, len(junction.road_list) - 1)
                    junction.road_list[turn_to].left_lane[-1] = self.right_lane[-1]
                    self.right_lane[-1] = None
            if self.right_lane[i] is not None and self.right_lane[i + 1] is None:
                self.right_lane[i + 1] = self.right_lane[i]
                self.right_lane[i] = None

    def show(self):
        # Draw road
        p.draw.line(screen, 'white', self.start, self.end, ROAD_WIDTH)
        
        # Draw lanes
        for i in range(self.length):
            # Compute the position of the current segment
            t = i / (self.length - 1)
            x = int(self.start[0] + t * (self.end[0] - self.start[0]))
            y = int(self.start[1] + t * (self.end[1] - self.start[1]))
            
            # Calculate lane positions
            angle = math.atan2(self.end[1] - self.start[1], self.end[0] - self.start[0])
            dx = math.cos(angle) * CAR_RADIUS
            dy = math.sin(angle) * CAR_RADIUS
            
            # Left and right lane offsets
            left_x = x - dy
            left_y = y + dx
            right_x = x + dy
            right_y = y - dx

            # Draw cars on the left lane
            if self.left_lane[i] is not None:
                pos_x, color_index = self.left_lane[i]
                p.draw.circle(screen, COLORS[color_index], (int(left_x - CAR_RADIUS // 2), int(left_y - CAR_RADIUS // 2)), CAR_RADIUS)

            # Draw cars on the right lane
            if self.right_lane[i] is not None:
                pos_x, color_index = self.right_lane[i]
                p.draw.circle(screen, COLORS[color_index], (int(right_x - CAR_RADIUS // 2), int(right_y - CAR_RADIUS // 2)), CAR_RADIUS)

def main():
    j = Junction()
    tick = 0
    r1 = Road((100, 400), (350, 400), None, j)
    r3 = Road((700, 400), (450, 400), None, j)
    r2 = Road((400, 100), (400, 350), None, j)
    r4 = Road((400, 700), (400, 450), None, j)

    road_list = [r1, r2, r3, r4]
    j.set_road_list(road_list, (400, 400))
    while True:
        tick += 1
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
        screen.fill(BLACK)
        j.draw()
        for road in road_list:
            road.update()
            road.show()
        p.display.flip()
        clock.tick(1)
        if tick % 10 == 0:
            j.current_side += 1
            j.current_side %= len(j.road_list)

if __name__ == '__main__':
    main()
