#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys
from math import fabs, sqrt, log10, exp


class Mandelbrot:

    def __init__(self):
        #
        # Start the mandelbrot set with the full image
        #
        self.xstart = -2.0
        self.xend = 2.0
        self.ystart = -2.0
        self.yend = 2.0

        #
        # For speed, just do a 400x400 dislpay
        #
        self.size = 400

        #
        # Our zoom in/out factor is 10, so we use 1/20th here
        # and apply it equally on both sides of the click.
        #
        self.zoomdist = 20.0

    def docalc(self):
        delta = (self.xend - self.xstart) / (1.0 * self.size)

        result = []
        y = 0
        yval = self.ystart
        while yval < self.yend:
            x = 0
            xval = self.xstart
            row = []
            while xval < self.xend:
                c = complex(xval, yval)
                z = complex(0.0, 0.0)
                for k in range(100):
                    z = z * z + c
                    if abs(z) >= 2.0:
                        break
                row.append(k)
                xval += delta
            result.append(row)
            yval += delta

        return result

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPointSize(1.0)
        glBegin(GL_POINTS)
        y = 0
        for row in self.mbrot:
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


    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, 400, 400, 0)
        glMatrixMode(GL_MODELVIEW)

    def mouse(self, button, state, x, y):
        if state != GLUT_DOWN:
            return

        dist = self.xend - self.xstart
        delta = dist / self.size
        xclick = self.xstart + x * delta
        yclick = self.ystart + y * delta

        if button == GLUT_LEFT_BUTTON:
            print("zooming in")
            factor = dist / self.zoomdist

        elif button == GLUT_RIGHT_BUTTON:
            print("zooming out")
            factor = dist * (self.zoomdist / 4.0)

        self.xstart = xclick - factor
        self.xend = xclick + factor
        self.ystart = yclick - factor
        self.yend = yclick + factor
        print("(%f, %f) (%f, %f)" % (self.xstart, self.xend, self.ystart, self.yend))

        self.mbrot = self.docalc()
        glutPostRedisplay()

    def main(self):
        self.mbrot = self.docalc()

        glutInit(sys.argv)
        glutInitWindowPosition(200, 300)
        glutInitWindowSize(400, 400)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutCreateWindow("Mandelbrot Set")
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutMouseFunc(self.mouse)

        glClearColor(0.2, 0.2, 0.2, 1.0)

        glutMainLoop()


if __name__ == "__main__":
    m = Mandelbrot()
    m.main()
