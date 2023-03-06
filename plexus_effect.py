import os
from random import randint, uniform
from math import sqrt
import colorsys
import pygame

# Set the position of the window to be centered on the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize pygame
pygame.init()

# Get the current display information
info = pygame.display.Info()

# Set the frames per second and screen size
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Set the speed at which the circles move and the maximum distance \
# at which they can connect
MOVE_SPEED = 0.8
MAX_DISTANCE = 200

# Set the screen to fullscreen and initialize the clock
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

'''
Define a class to create and manage the circles
'''
class Circle:
    def __init__(self, quantity):
        self.quantity = quantity
        self.circles = []
        self.velocity = [MOVE_SPEED, MOVE_SPEED]
        self.create_circles()

    '''
    Create the circles with random positions and velocities
    '''
    def create_circles(self):
        for _ in range(self.quantity):
            x = randint(0, SCREEN_WIDTH)
            y = randint(0, SCREEN_HEIGHT)
            velocity_x = uniform(-self.velocity[0], self.velocity[0])
            velocity_y = uniform(-self.velocity[1], self.velocity[1])
            position = (x, y, velocity_x, velocity_y)
            self.circles.append(position)

    '''
    Update the position of each circle based on its velocity
    '''
    def update(self):
        for i in range(self.quantity):
            x, y, velocity_x, velocity_y = self.circles[i]
            x += velocity_x
            y += velocity_y

            # If the circle hits a screen edge, reverse its velocity
            if x >= SCREEN_WIDTH or x <= 0:
                velocity_x *= -1

            if y >= SCREEN_HEIGHT or y <= 0:
                velocity_y *= -1

            self.circles[i] = (x, y, velocity_x, velocity_y)

    '''
    Find all pairs of circles within the maximum distance
    and return their positions as line segments
    '''
    def connect_circles(self):
        return [((circle1[0], circle1[1]), (circle2[0], circle2[1]))
                for i, circle1 in enumerate(self.circles)
                for _, circle2 in enumerate(self.circles[i+1:])]

'''
Define a function to generate colors
based on the distance between circles
'''
def color(distance, max_distance, h, s, v):
    # Convert the input hue to an RGB value
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    # Adjust the RGB values based on the distance between the circles
    r, g, b = tuple(round((max_distance - distance) * i * 255 / max_distance) for i in (r, g, b))
    return r, g, b

'''
Define a function to convert HSV colors to RGB colors
'''
def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Create the circles object
circles = Circle(100)

'''
Define the main function that runs the animation
'''
def plexus():
    print(info)

    # Initialize the hue and pause variables
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