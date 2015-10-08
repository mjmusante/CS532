#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math
import sys

Width = 640
Height = 480
BoundingBox = 500.0

def plotPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()


class Liner:
    def __init__(self):
        self.prev = False

    def start(self):
        glBegin(GL_LINES)

    def end(self):
        glEnd()

    def goto(self, x, y):
        (x, y) = (int(round(x)), int(round(y)))
        if self.prev:
            glVertex2i(*self.prev)
            glVertex2i(x, y)
        self.prev = (x, y)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # x-axis in Red
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(-BoundingBox, 0)
    glVertex2f(BoundingBox, 0)
    glEnd()

    # y-axis in Green
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(0, -BoundingBox)
    glVertex2f(0, BoundingBox)
    glEnd()

    #
    # The equation to convert:
    #
    #   (x^2 + y^2 + 2ax)^2 = 4a^2(x^2 + y^2)
    #
    # Substitutions:
    #   r^2 = x^2 + y^2
    #   x = r * cos(theta)
    #   y = r * sin(theta)
    #
    #   (r^2 + 2ar cos(theta))^2 = 4a^2r^2
    #
    # Solving for r:
    #
    #   r^2 + 2ar cos(theta) = 2ar
    #   r + 2a cos(theta) = 2a
    #   r = 2a(1 - cos(theta)
    #


    l = Liner()
    a = 100
    theta = 0.0
    delta_theta = 2 * math.pi / 1000.0

    glColor3f(1.0, 1.0, 1.0)
    l.start()
    while theta < 2 * math.pi:
        r = 2.0 * a * (1.0 - math.cos(theta))
        l.goto(r * math.cos(theta), r * math.sin(theta))
        theta += delta_theta
    l.end()


    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if width > height:
        boxh = BoundingBox
        boxw = BoundingBox * width / height
    else:
        boxw = BoundingBox
        boxh = BoundingBox * height / width
    gluOrtho2D(-boxw, boxw, boxh, -boxh)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(Width, Height)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("Homework 3: Question 1a")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
