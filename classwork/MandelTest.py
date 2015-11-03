#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys

from math import fabs, sqrt, log10, exp


def docalc(xstart, xend, ystart, yend, size):
    delta = (xend - xstart) / (1.0 * size)

    result = []
    y = 0
    yval = ystart
    while yval < yend:
        x = 0
        xval = xstart
        row = []
        while xval < xend:
            c = complex(xval, yval)
            z = complex(0.0, 0.0)
            for k in range(100):
                z = z * z + c
                if abs(z) >= 2.0:
                    break
            row.append(k)
            xval += delta

#            real = 0.0
#            img = 0.0
#            k = 0
#            while fabs(sqrt(real * real + img * img)) < 2.0 and k < 256:
#                real = real * real - img * img + xval
#                img = 2 * real * img + yval
#                k += 1
#            row.append(k)
#            xval += delta

        result.append(row)
        yval += delta

    return result

mbrot = docalc(-2.0, 2.0, -2.0, 2.0, 400)

def plotPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPointSize(1.0)
    glBegin(GL_POINTS)
    y = 0
    for row in mbrot:
        x = 0
        for val in row:
            r = int((val / 100.0) * 256.0)
            rval = r
            if r == 0:
                rval = 1
            g = int(log10(0.65 * rval * 10.0) * 256.0)
            b = int(exp(-0.15 * val) * 256.0)
            glColor3ub(r, g, b)
            glVertex2i(x, y)
            x += 1
        y += 1
    glEnd()


    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 400, 400, 0)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(400, 400)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("GLUT Window")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
