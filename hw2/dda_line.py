#! /usr/bin/python

from __future__ import division

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math
import sys

def plotPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()


def draw_dda_line(p1x, p1y, p2x, p2y):
    dy = p2y - p1y
    dx = p2x - p1x
    if abs(dx) > abs(dy):
        step = abs(dx)
    else:
        step = abs(dy)

    print("Slope = %.2f" % (dy / dx))
    dx = dx / step
    dy = dy / step

    x = p1x
    y = p1y
    plotPixel(round(x), round(y))
    for f in range(1, step):
        x += dx
        y += dy
        plotPixel(round(x), round(y))



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.4, 1.0, 0.0)
    draw_dda_line(1, 2, 100, 80)
    draw_dda_line(10, 60, 30, 10)
    draw_dda_line(102, 101, 180, 200)
    draw_dda_line(110, 130, 160, 110)
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
