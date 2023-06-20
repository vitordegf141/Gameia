import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math
from game_object import Triangle, Circle, Square
from game_data import GameData
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
text_size =32
gamedata : GameData = GameData(window_width,window_height)
text_read=""
# Square position variables
square_x = 400
square_y = 300

# Circle position variables
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
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()    
    glOrtho(0, window_width, 0, window_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glClearColor(0, 0, 0, 1)

def create_initial_circles():
    global next_circle_time
    global gamedata
    for _ in range(num_circles):
        gamedata.add_circle()
    current_time = pygame.time.get_ticks()
    next_circle_time = current_time + random.randint(2000, 10000)

def create_random_circle():
    global next_circle_time
    global gamedata
    current_time = pygame.time.get_ticks()
    if current_time >= next_circle_time:
        gamedata.add_circle()
        next_circle_time = current_time + random.randint(2000//len(gamedata.triangles), 10000//len(gamedata.triangles))  # Random time between 2s and 10s



def draw_square():    
    gamedata.square.draw()

def draw_circles():
    for circle in gamedata.circles:
        circle.draw()

def draw_triangle():
    for triangle in gamedata.triangles:
        triangle.draw()

def load_image(file_path):
    try:
        image = pygame.image.load(file_path)
        return image.convert_alpha()
    except pygame.error:
        print(f"Unable to load image: {file_path}")
        return None

def render_texts(texts : list):
    global text_size,gamedata
    height_used =0
    for text in texts:
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=((text_surface.get_width()//2)+(gamedata.square.x )-(window_width//2)+2,  gamedata.square.y - text_surface.get_height() -height_used   +(window_height//2) ))
        height_used += text_surface.get_height()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glRasterPos2f(text_rect.x, text_rect.y)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE,
                    pygame.image.tostring(text_surface, "RGBA", True))
        glDisable(GL_BLEND)

def get_timer_text(elapsed_time):
    return f"Time: {elapsed_time} seconds"

def get_game_score():
    text=""
    for triangle in gamedata.triangles:
        text+="#"+str(triangle.points)
    text+= "n of circles:"+str(len(gamedata.circles))
    return text

def check_collision():
    global game_over,gamedata
    for triangle in gamedata.triangles:
        for circle in gamedata.circles:
            distance = math.sqrt((circle.x - triangle.x) ** 2 + (circle.y - triangle.y) ** 2)
            if distance < circle.radius + triangle.size / 2:
                if triangle.eat_circle(circle) :
                    gamedata.triangles.append((Triangle(triangle.x, triangle.y, triangle_size-10, (random.random(), random.random(), random.random()))))
                gamedata.circles.remove(circle)

def move_triangle():
    global gamedata
    if game_over:
        return
    for triangle in gamedata.triangles:
        if triangle.freeze >0:
            triangle.freeze -=1
            continue
        if(len(gamedata.triangles)>1):
            triangle.hungry -=1
            if(triangle.hungry <=0):
                triangle.die = True
        closest_circle = find_closest_circle(triangle)
        if closest_circle:
            dx = closest_circle.x - triangle.x
            dy = closest_circle.y - triangle.y
            angle = math.atan2(dy, dx)
            speed = 2
            triangle.x += speed * math.cos(angle)
            triangle.y += speed * math.sin(angle)

def find_closest_circle(triangle :Triangle):
    if gamedata.circles:
        closest_circle = min(gamedata.circles, key=lambda c: math.sqrt((c.x - triangle.x) ** 2 + (c.y - triangle.y) ** 2))
        return closest_circle
    return None

def handle_key_events():
    global square_x, square_y, is_paused,text_size,font,gamedata,text_read
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
            elif event.unicode >='a' and event.unicode <='z' or event.unicode ==' ':
                if is_paused:
                    text_read += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                # Handle the click event based on the mouse position
                handle_click(mouse_x, mouse_y)
        
    keys = pygame.key.get_pressed()

    # Move the square based on key inputs
    if not is_paused:
        if keys[K_w]:
            gamedata.square.y += 5
        if keys[K_s]:
            gamedata.square.y -= 5
        if keys[K_a]:
            gamedata.square.x -= 5
        if keys[K_d]:
            gamedata.square.x += 5
    if keys[K_z]:
        if(text_size>2):
            text_size -= 1
            font = pygame.font.Font('freesansbold.ttf', text_size)
    if keys[K_x]:
        if(text_size<48):
            text_size += 1
            font = pygame.font.Font('freesansbold.ttf', text_size)

def handle_click(mouse_x, mouse_y):
    # Check if the mouse position is within a certain object's boundaries
    print(f"square_x = ({gamedata.square.x},{gamedata.square.x + gamedata.square.width}) , square_y = ({gamedata.square.y},{gamedata.square.y + gamedata.square.height}) ")
    print(f"mouse = ({mouse_x},{mouse_y})")
    if gamedata.square.x < mouse_x < gamedata.square.x + gamedata.square.width and gamedata.square.y < mouse_y < gamedata.square.y + gamedata.square.height:
        # Perform actions for the square on-click
        print("Square clicked!")


def game_loop():
    global square_x, square_y, text_size, font, gamedata,window_width,window_height
    gamedata.square = Square(square_x, square_y, square_size, (1, 1, 1),"humand_crop.png")
    gamedata.triangles.append(Triangle(triangle_x, triangle_y, triangle_size, (1, 1, 0)))
    
    create_initial_circles()
    font = pygame.font.Font('freesansbold.ttf', text_size)
    while True:
        texts=[]
        gamedata.triangles = list(filter(lambda t: t.die ==False,gamedata.triangles))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        handle_key_events()

        if not is_paused:
            check_collision()
            move_triangle()
            create_random_circle()
        
        glLoadIdentity()
        glTranslatef(-gamedata.square.x +(window_width//2), -gamedata.square.y +(window_height//2), 0)
        draw_circles()
        draw_triangle()
        draw_square()

        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000
        
        texts.append(get_timer_text(elapsed_time))
        texts.append(text_read)
        texts.append(get_game_score())
        render_texts(texts)
        pygame.display.flip()
        
        pygame.time.wait(10)

if __name__ == '__main__':
    init()
    game_loop()
