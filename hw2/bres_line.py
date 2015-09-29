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


def draw_bres_line(p1x, p1y, p2x, p2y):
    dx = p2x - p1x
    if dx == 0:
        # special-case code for vertical lines
        if dy > 0:
            y = p1y
            end = p2y
        else:
            y = p2y
            end = p1y
        while y < end:
            plotPixel(p1x, y)
            y += 1
        return

    dy = p2y - p1y
    k = math.fabs(dy / dx)
    p = 2 * (dy - dx)

    c1 = 2 * dy
    c2 = 2 * (dy - dx)

    if p1x > p2x:
        x = p2x
        y = p2y
        end = p1x
    else:
        x = p1x
        y = p1y
        end = p2x

    err = 0.0
    while x < end:
        plotPixel(x, y)
        err += k
        while err >= 0.5:
            plotPixel(x, y)
            if dy < 0:
                y -= 1
            elif dy > 0:
                y += 1
            err -= 1.0
        x += 1


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.4, 1.0, 0.0)

    # Check different slopes
    draw_bres_line(1, 2, 100, 80)        # slope ~=  0.79
    draw_bres_line(10, 60, 30, 10)       # slope ~= -2.5
    draw_bres_line(102, 101, 180, 200)   # slope ~=  1.27
    draw_bres_line(110, 130, 160, 110)   # slope ~= -0.40

    # Check vertical and horizontal lines
    draw_bres_line(50, 300, 70, 300)     # horizontal, increasing x
    draw_bres_line(50, 300, 30, 300)     # horizontal, decreasing x
    draw_bres_line(50, 300, 50, 280)     # vertical, decreasing y
    draw_bres_line(50, 300, 50, 320)     # vertical, increasing y

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
