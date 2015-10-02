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
# This function uses Bresenham's algorithm for drawing lines. There
# are three cases to deal with:
#
#   1.  A vertical line (dx == 0). This is a special case where
#       we just draw a straight line from the start to the end.
#
#   2.  The line is more vertical than horizintal (|dy| > |dx|).
#       For this case, we flip Breshanham's algorithm on its side
#       and walk from y1 to y2, filling in all the x coordinates
#       along the way.
#
#   3.  The line is more horizontal than vertical (|dx| > |dy|).
#       For this case, we just use the standard algorithm,
#       walking the x-axis from x1 to x2 and fill in the y
#       coordinates along the way.
#
def draw_bres_line(p1x, p1y, p2x, p2y):
    dx = p2x - p1x
    dy = p2y - p1y
    if dx == 0:
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

    if abs(dy) > abs(dx):

        # flip the coordinates if needed
        if p1y > p2y:
            x = p2x
            p2x = p1x
            p1x = x
            y = p2y
            p2y = p1y
            p1y = y
            dx = p2x - p1x
            dy = p2y - p1y
        else:
            x = p1x
            y = p1y

        # calculate the end points and the p, c1, and c2 values
        endx = p2x
        endy = p2y
        dx = abs(dx)
        p = 2 * dx - dy
        c1 = 2 * dx
        c2 = 2 * (dx - dy)

        # Are we increasing or decreasing x?
        delta = 1
        if x > endx:
            delta = -1

        # loop over the y axis and plot points along the x axis
        plotPixel(x, y)
        while y < endy:
            y += 1
            if p < 0:
                p += c1
            else:
                p += c2
                x += delta
            plotPixel(x, y)

    else:

        # flip the coordinates if needed
        if p1x > p2x:
            x = p2x
            p2x = p1x
            p1x = x
            y = p2y
            p2y = p1y
            p1y = y
            dx = p2x - p1x
            dy = p2y - p1y
        else:
            x = p1x
            y = p1y

        # calculate the end points and the p, c1, and c2 values
        endx = p2x
        endy = p2y
        dy = abs(dy)
        p = 2 * dy - dx
        c1 = 2 * dy
        c2 = 2 * (dy - dx)

        # Are we increasing or decreasing y?
        delta = 1
        if y > endy:
            delta = -1

        # loop over the x axis and plot points along the y axis
        plotPixel(x, y)
        while x < endx:
            x += 1
            if p < 0:
                p += c1
            else:
                p += c2
                y += delta
            plotPixel(x, y)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw the lines
    glColor3f(0.0, 0.4, 1.0)
    for i in point_list:
        draw_bres_line(*i)


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
