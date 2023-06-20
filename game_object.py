import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy
import random
import math

class GameObject:
    def __init__(self, x, y, color,image_path=None):
        self.x = x
        self.y = y
        self.color = color
        self.texture_id=None
        if(image_path!=None):
            self.texture_id = self.load_texture(image_path)

    def load_texture(self, image_path):
        try:
            image = pygame.image.load(image_path)
            image_data = pygame.image.tostring(image, "RGBA", True)
            #raw_data = image_data.get_buffer().raw
            data = numpy.fromstring(image_data, numpy.uint8)
            width, height = image.get_rect().size
            self.width= width
            self.height =height
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

            return texture_id
        except pygame.error:
            print(f"Unable to load image: {image_path}")
            return None

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
    def __init__(self, x, y, size, color,image_path=None):
        super().__init__(x, y, color,image_path)
        self.size = size
    def draw(self):
        if self.texture_id:
            white = (1,1,1)
            glColor3f(*white)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(self.x, self.y)
            glTexCoord2f(1, 0)
            glVertex2f(self.x + self.width, self.y)
            glTexCoord2f(1, 1)
            glVertex2f(self.x + self.width, self.y + self.height)
            glTexCoord2f(0, 1)
            glVertex2f(self.x, self.y + self.height)
            glEnd()
            glDisable(GL_TEXTURE_2D)
        else:
            glColor3f(*self.color)
            glBegin(GL_QUADS)
            glVertex2f(self.x - self.size / 2, self.y - self.size / 2)
            glVertex2f(self.x + self.size / 2, self.y - self.size / 2)
            glVertex2f(self.x + self.size / 2, self.y + self.size / 2)
            glVertex2f(self.x - self.size / 2, self.y + self.size / 2)
            glEnd()
