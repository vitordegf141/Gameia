import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math
from game_object import Triangle, Circle, Square

pygame.font.init()

start_time = pygame.time.get_ticks()
font = pygame.font.Font('freesansbold.ttf', 32)

# Window and shape dimensions
window_width = 1000
window_height = 800
square_size = 50
circle_radius = 20
triangle_size = 40
screen = None

# Square position variables
square_x = 400
square_y = 300

# Circle position variables
circles = []
num_circles = 5

# Triangle position variables
triangle_x = window_width // 2
triangle_y = window_height // 2

# Game state variables
game_over = False
timer = 0
next_circle_time = random.randint(10, 60) * 1000  # Random time between 10s and 1min
is_paused = False

def init():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((window_width, window_height), DOUBLEBUF | OPENGL)

    glOrtho(0, window_width, 0, window_height, -1, 1)
    glClearColor(0, 0, 0, 1)

def create_initial_circles():
    global circle_radius
    for _ in range(num_circles):
        while True:
            circle_x = random.randint(circle_radius, window_width - circle_radius)
            circle_y = random.randint(circle_radius, window_height - circle_radius)
            circle_radius = random.randint(20, 40)
            if not check_overlap(circle_x, circle_y, circle_radius):
                circles.append(Circle(circle_x, circle_y, (0, 1, 0)))
                break

def create_random_circle():
    global next_circle_time, circle_radius
    current_time = pygame.time.get_ticks()
    if current_time >= next_circle_time:
        circle_x = random.randint(circle_radius, window_width - circle_radius)
        circle_y = random.randint(circle_radius, window_height - circle_radius)
        circle_radius = random.randint(20, 40)
        if not check_overlap(circle_x, circle_y, circle_radius):
            circles.append(Circle(circle_x, circle_y, (0, 1, 0)))
            next_circle_time = current_time + random.randint(2000, 10000)  # Random time between 2s and 10s

def create_circles():
    global next_circle_time, timer
    timer += pygame.time.get_ticks() - next_circle_time
    if timer >= next_circle_time:
        circle_x = random.randint(circle_radius, window_width - circle_radius)
        circle_y = random.randint(circle_radius, window_height - circle_radius)
        circle_radius = random.randint(20, 40)
        if not check_overlap(circle_x, circle_y, circle_radius):
            circles.append(Circle(circle_x, circle_y, (0, 1, 0)))
            next_circle_time = random.randint(2000, 10000)  # Random time between 2s and 10s
            timer = 0

def check_overlap(x, y, radius):
    for circle in circles:
        distance = math.sqrt((circle.x - x) ** 2 + (circle.y - y) ** 2)
        if distance < circle.radius + radius:
            return True
    if (
        square_x < x + radius and
        square_x + square_size > x - radius and
        square_y < y + radius and
        square_y + square_size > y - radius
    ):
        return True
    return False

def draw_square():
    square = Square(square_x, square_y, square_size, (1, 1, 1))
    square.draw()

def draw_circles():
    for circle in circles:
        circle.draw()

def draw_triangle():
    triangle = Triangle(triangle_x, triangle_y, triangle_size, (1, 0, 0))
    triangle.draw()

def draw_timer(elapsed_time):
    text_surface = font.render(f"Time: {elapsed_time} seconds", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2))
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glRasterPos2f(text_rect.x, text_rect.y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE,
                pygame.image.tostring(text_surface, "RGBA", True))
    glDisable(GL_BLEND)

def check_collision():
    global game_over
    for circle in circles:
        distance = math.sqrt((circle.x - triangle_x) ** 2 + (circle.y - triangle_y) ** 2)
        if distance < circle.radius + triangle_size / 2:
            circles.remove(circle)

def move_triangle():
    global triangle_x, triangle_y
    if not game_over:
        closest_circle = find_closest_circle()
        if closest_circle:
            dx = closest_circle.x - triangle_x
            dy = closest_circle.y - triangle_y
            angle = math.atan2(dy, dx)
            speed = 2
            triangle_x += speed * math.cos(angle)
            triangle_y += speed * math.sin(angle)

def find_closest_circle():
    if circles:
        closest_circle = min(circles, key=lambda c: math.sqrt((c.x - triangle_x) ** 2 + (c.y - triangle_y) ** 2))
        return closest_circle
    return None

def handle_key_events():
    global square_x, square_y, is_paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == pygame.K_PAUSE:
                is_paused = not is_paused

    keys = pygame.key.get_pressed()

    # Move the square based on key inputs
    if keys[K_w]:
        square_y += 5
    if keys[K_s]:
        square_y -= 5
    if keys[K_a]:
        square_x -= 5
    if keys[K_d]:
        square_x += 5

def game_loop():
    create_initial_circles()
    global square_x, square_y
    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        handle_key_events()

        if not is_paused:
            check_collision()
            move_triangle()
            create_random_circle()

        draw_square()
        draw_circles()
        draw_triangle()

        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000
        draw_timer(elapsed_time)

        pygame.display.flip()
        glClearColor(0, 0, 0, 1)
        pygame.time.wait(10)

if __name__ == '__main__':
    init()
    game_loop()
