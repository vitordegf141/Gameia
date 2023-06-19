import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pass


class Triangle(GameObject):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, color)
        self.size = size

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_TRIANGLES)
        glVertex2f(self.x, self.y + self.size / 2)
        glVertex2f(self.x - self.size / 2, self.y - self.size / 2)
        glVertex2f(self.x + self.size / 2, self.y - self.size / 2)
        glEnd()


class Circle(GameObject):
    radius = 20  # Class variable

    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(self.x, self.y)
        for i in range(61):
            angle = 2 * math.pi * i / 60
            x = self.x + Circle.radius * math.cos(angle)
            y = self.y + Circle.radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()


class Square(GameObject):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, color)
        self.size = size

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f(self.x - self.size / 2, self.y - self.size / 2)
        glVertex2f(self.x + self.size / 2, self.y - self.size / 2)
        glVertex2f(self.x + self.size / 2, self.y + self.size / 2)
        glVertex2f(self.x - self.size / 2, self.y + self.size / 2)
        glEnd()
