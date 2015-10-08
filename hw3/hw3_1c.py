#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math
import sys

Width = 640
Height = 480
BoundingBox = 32.0

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
        if self.prev:
            glVertex2f(*self.prev)
            glVertex2f(x, y)
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
    #   y = x * tan((x^2 + y^2) / a)
    #
    # Substitutions:
    #   r^2 = x^2 + y^2
    #   x = r * cos(theta)
    #   y = r * sin(theta)
    #
    #   r * sin(theta) = r * cos(theta) * tan(r^2 / a)
    #
    # Solving for r:
    #
    #   sin(theta) = cos(theta) * sin(r^2 /a) / cos(r^2 / a)
    #   sin(theta) / cos(theta) = sin(r^2 / a) / cos(r^2 / a)
    #   theta = r^2 / a
    #   r = +/- sqrt(a * theta)


    a = 100
    delta_theta = 2 * math.pi / 1000.0

    glColor3f(0.5, 1.0, 1.0)
    l = Liner()
    l.start()
    theta = 0.0
    while theta < 2 * math.pi:
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        r = math.sqrt(theta * a)
        l.goto(r * cos_t, r * sin_t)
        theta += delta_theta
    l.end()

    glColor3f(1.0, 0.5, 1.0)
    l = Liner()
    l.start()
    theta = 0.0
    while theta < 2 * math.pi:
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        r = -math.sqrt(theta * a)
        l.goto(r * cos_t, r * sin_t)
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
    glutCreateWindow("GLUT Window")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
