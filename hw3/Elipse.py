#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math
import sys

Width = 640
Height = 480

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
    glVertex2i(-Width, 0)
    glVertex2i(Width, 0)
    glEnd()

    # y-axis in Green
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2i(0, -Height)
    glVertex2i(0, Height)
    glEnd()


    l = Liner()
    theta = 0.0
    delta_theta = 2 * math.pi / 1000.0

    # draw an elipse with major axis 100, minor axis 50
    a = 100
    b = 50
    glColor3f(1.0, 1.0, 1.0)
    l.start()
    while theta < 2 * math.pi:
        asin = a * math.sin(theta)
        bcos = b * math.cos(theta)

        r = (a * b) / math.sqrt(bcos * bcos + asin * asin)
        l.goto(r * math.cos(theta), r * math.sin(theta))
        theta += delta_theta
    l.end()


    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-Width, Width, Height, -Height)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(Width, Height)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("GLUT Window")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
