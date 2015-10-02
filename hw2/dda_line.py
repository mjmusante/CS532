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



#
# DDA line drawing algorithm
#
def draw_dda_line(p1x, p1y, p2x, p2y):
    dy = p2y - p1y
    dx = p2x - p1x
    if abs(dx) > abs(dy):
        step = abs(dx)
    else:
        step = abs(dy)

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

    # draw the lines
    glColor3f(0.0, 0.4, 1.0)
    for i in point_list:
        draw_dda_line(*i)


    # draw the points of each line so we can see visually
    # in the window if the lines are connecting the dots
    glColor3f(0.4, 1.0, 0.0)
    for i in point_list:
        plotPixel(i[0], i[1])
        plotPixel(i[2], i[3])

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
