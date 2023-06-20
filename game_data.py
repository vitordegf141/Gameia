from game_object import *


class GameData :
    def __init__(self,window_width,window_height):
        self.circles : list[Circle] = []
        self.square : Square = None
        self.triangles : list[Triangle] = []
        self.window_width =window_width
        self.window_height = window_height
        self.field : Field = Field(2024)

    def add_circle(self):
        tries = 0
        circle_x = random.randint(Circle.radius, self.field.size - Circle.radius)
        circle_y = random.randint(Circle.radius, self.field.size - Circle.radius)
        while(tries <3 and not self.check_overlap(circle_x, circle_y, Circle.radius)):
            tries +=1
            circle_x = random.randint(Circle.radius, self.field.size - Circle.radius)
            circle_y = random.randint(Circle.radius, self.field.size - Circle.radius)
        self.circles.append(Circle(circle_x, circle_y, (0, 1, 0)))

    def check_overlap(self,x, y, radius):
        for circle in self.circles:
            distance = math.sqrt((circle.x - x) ** 2 + (circle.y - y) ** 2)
            if distance < circle.radius + radius:
                return True
            if (
                self.square.x < x + radius and
                self.square.x + self.square.size > x - radius and
                self.square.y < y + radius and
                self.square.y + self.square.size > y - radius
            ):
                return True
            return False

class Field:
    def __init__(self, size):
        self.size =size

class camera:
    pass