#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys

def plotPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.4, 1.0, 0.0)
    for x in range(-320, 320):
        y = (x - 10) * (x + 10) / 10
        if y > -240 and y < 240:
            plotPixel(x, y)
    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-width, width, height, -height)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(640, 480)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("GLUT Window")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
