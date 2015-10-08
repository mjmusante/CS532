#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys


def drawFigure(x, y):
    glShadeModel(GL_SMOOTH)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    for i in range(0, 4):
        glVertex2f(x[i], y[i])
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    X = [200.0, 300.0, 300.0, 200.0]
    Y = [200.0, 200.0, 300.0, 300.0]

    glColor3f(1.0, 0.5, 1.0)

    drawFigure(X, Y);

    a = 0.71
    b = -0.71
    c = 0.71
    d = 0.71
    tx = 100.0
    ty = 50.0

    Xn = [0.0, 0.0, 0.0, 0.0]
    Yn = [0.0, 0.0, 0.0, 0.0]

    for i in range(0, 4):
        Xn[i] = a * X[i] + b * Y[i] + tx
        Yn[i] = c * X[i] + d * Y[i] + ty

    glColor3f(0.5, 1.0, 0.1)
    drawFigure(Xn, Yn)

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)
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
