#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import random
import sys

class Fern:
    def __init__(self):
        self.points = ()
        minx = 0
        miny = 0
        maxx = 0
        maxy = 0

        for j in range(1, 10000):
            x = random.random()
            y = random.random()

            for i in range(1, 50):
                p = random.random()

                if p < 0.01:
                    (xn, yn) = (0, 0.16 * y)
                elif p < 0.08:
                    (xn, yn) = (0.2*x - 0.26*y, 0.23*x + 0.22*y + 1.6)
                elif p < 0.15:
                    (xn, yn) = (-0.15*x + 0.28*y, 0.26*x + 0.24*y + 0.44)
                else:
                    (xn, yn) = (0.85*x + 0.04*y, -0.04*x + 0.85*y + 1.6)
                (x, y) = (xn, yn)
            self.points += ((x, -y),)
            minx = min(x, minx)
            maxx = max(x, maxx)
            miny = min(y, miny)
            maxy = max(y, maxy)

        self.y_size = maxy - miny
        self.x_size = maxx - minx


    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.4, 1.0, 0.0)

        glBegin(GL_POINTS)
        for i in self.points:
            glVertex2f(*i)
        glEnd()

        glutSwapBuffers()


    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
 
        # calculate best ortho to keep the image square
#        if width > height:
#            y_size = self.y_size
#            x_size = self.x_size * width / height
#        else:
#            x_size = self.x_size
#            y_size = self.y_size * height / width
        gluOrtho2D(-self.x_size, self.x_size, 0.0, -self.y_size)
        glMatrixMode(GL_MODELVIEW)


    def keyboard(self, a, b, c):
        sys.exit(0)

    def main(self):
        glutInit(sys.argv)
        glutInitWindowPosition(200, 300)
        glutInitWindowSize(640, 480)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutCreateWindow("GLUT Window")
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)

        glClearColor(0.2, 0.2, 0.2, 1.0)

        glutMainLoop()


if __name__ == "__main__":
    fern = Fern()
    fern.main()
