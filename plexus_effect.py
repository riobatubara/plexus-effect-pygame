import os
from random import randint, uniform
from math import sqrt
import colorsys
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w,info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

FPS = 60
MOVE_SPEED = 0.8
MAX_DISTANCE = 200

class Circle:
    def __init__(self, quantity):
        self.quantity = quantity
        self.circles = []
        self.velocity = [MOVE_SPEED, MOVE_SPEED]
        self.create_circles()

    def create_circles(self):
        for _ in range(self.quantity):
            self.x = randint(0, SCREEN_WIDTH)
            self.y = randint(0, SCREEN_HEIGHT)
            self.velocity_x = uniform(-self.velocity[0], self.velocity[0])
            self.velocity_y = uniform(-self.velocity[1], self.velocity[1])
            self.position = (self.x, self.y, self.velocity_x, self.velocity_y)
            self.circles.append(self.position)

    def update(self):
        self.circles_moved = []

        for i in self.circles:
            self.x = i[0]
            self.y = i[1]

            self.velocity_x = i[2]
            self.velocity_y = i[3]

            self.x += self.velocity_x
            self.y += self.velocity_y

            if self.x >= SCREEN_WIDTH or self.x <= 0:
                self.velocity_x *= -1

            if self.y >= SCREEN_HEIGHT or self.y <= 0:
                self.velocity_y *= -1

            self.position = (self.x, self.y, self.velocity_x, self.velocity_y)
            self.circles_moved.append(self.position)
            self.circles = self.circles_moved

    def connect_circles(self):
        self.lines = []
        for point1 in range(self.quantity - 1):
            for point2 in range(point1 + 1, self.quantity):
                self.lines.append([self.circles[point1][:2], self.circles[point2][:2]])

        return self.lines


# Rendering colors by distance
def color(distance, max_distance, h, s, v):
    h_max, s_max, v_max = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))
    r = int((max_distance - distance) * h_max / max_distance)
    g = int((max_distance - distance) * s_max / max_distance)
    b = int((max_distance - distance) * v_max / max_distance)
    return r, g, b


# The HSV converting to RGB function
def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Initiate object
circles = Circle(100)

def plexus():
    print(info)

    hue = 0
    paused = False
    running = True
    while running:
        clock.tick(FPS)
        pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")

        screen.fill((0, 0, 0))

        r, g, b = hsv2rgb(hue, 1, 1)

        for i in circles.connect_circles():
            start_position = i[0]
            end_position = i[1]
            distance = sqrt((start_position[0] - end_position[0])
                ** 2 + (start_position[1] - end_position[1]) ** 2)

            if distance < MAX_DISTANCE:
                r, g, b = color(distance, MAX_DISTANCE, hue, 1, 1)
                pygame.draw.line(screen, (r, g, b), start_pos=i[0], end_pos=i[1], width=2)

        for i in circles.circles:
            pygame.draw.circle(screen, (r, g, b), center=i[:2], radius=3)

        hue += 0.001
        if hue >= 1.0:
            hue = 0

        circles.update()

        if not paused:
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    paused = not paused

if __name__ == "__main__":
    plexus()
