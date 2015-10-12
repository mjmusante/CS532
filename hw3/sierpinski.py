#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math
import random
import sys

class Fern:
    def __init__(self):
        self.points = ()

        x = 0.0
        y = 0.0
        sq34 = math.sqrt(3.0) / 4.0

        for j in range(1, 20000):

            p = random.random()

            if p < 0.3333:
                (xn, yn) = (0.5*x, 0.5*y)
            elif p < 0.6666:
                (xn, yn) = (0.5*x + 0.25, 0.5*y + sq34)
            else:
                (xn, yn) = (0.5*x + 0.5, 0.5*y)
            (x, y) = (xn, yn)
            self.points += ((x, -y),)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.4, 0.4, 1.0)

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
        if width > height:
            y_size = 1.0
            x_size = 1.0 * width / height
        else:
            x_size = 1.0
            y_size = 1.0 * height / width
        gluOrtho2D(0.0, x_size, 0.0, -y_size)
        glMatrixMode(GL_MODELVIEW)


    def main(self):
        glutInit(sys.argv)
        glutInitWindowPosition(200, 300)
        glutInitWindowSize(640, 480)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutCreateWindow("GLUT Window")
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)

        glClearColor(0.2, 0.2, 0.2, 1.0)

        glutMainLoop()


if __name__ == "__main__":
    fern = Fern()
    fern.main()
