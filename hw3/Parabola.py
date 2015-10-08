#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

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

    def lineTo(self, x, y):
        if self.prev:
            glBegin(GL_LINES)
            glVertex2i(*self.prev)
            glVertex2i(x, y)
            glEnd()
        self.prev = (x, y)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.4, 1.0, 0.0)
    l = Liner()
    for x in range(-Width, Width):
        y = (x - 10) * (x + 10) / 10
        if y > - Height and y < Height:
            l.lineTo(x, y)
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
