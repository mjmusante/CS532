#! /usr/bin/python

from __future__ import division

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math
import sys

point_list = (
        (0, 0, 100, -200),      # negative slope, |m| > 1
        (50, -20, 80, -40),     # negative slope, |m| < 1
        (30, -60, 60, -40),     # positive slope, |m| < 1
        (10, -70, 85, 10),      # positive slope, |m| > 1
        (50, 300, 70, 300),     #     zero slope, increasing x
        (50, 300, 30, 300),     #     zero slope, decreasing x
        (50, 300, 50, 280),     # infinite slope, decreasing y
        (50, 300, 50, 320),     # infinite slope, increasing y
        )

def plotPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()


def draw_bres_line(p1x, p1y, p2x, p2y):
    dx = p2x - p1x
    dy = p2y - p1y
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

    for i in point_list:
        draw_bres_line(*i)

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

    for i in point_list:
        (x1, y1, x2, y2) = i
        if x2 - x1 == 0:
            print("Slope %s: infinite" % (i,))
        else:
            print("Slope %s: %.2f" % (i, (y2 - y1) / (x2 - x1)))

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
