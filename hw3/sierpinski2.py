#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math
import random
import sys

class Sierpinski:

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.4, 0.4, 1.0)

        # We can draw sierpinski's fractal by plotting only the
        # odd numbers of pascal's triangle.
        #
        # As we only need to know if the number is odd or even,
        # and the exact value doesn't matter, we can simplify
        # by these rules:
        #
        #   even + even = even
        #   even + odd = odd
        #   odd + even = odd
        #   odd + odd = even
        #
        # This is known in computer science as an XOR operation,
        # so all we need to do is keep track of one row at a time
        # and generate the values for the next row as we work our
        # way along the current row.

        # start with an empty array
        calc = []


        glBegin(GL_POINTS)
        for row in range(0, self.height):

            # first pixel is always true
            calc.insert(0, True)

            # work our way along the current row
            for col in range(0, min(len(calc), self.width)):

                # plot a pixel if the value is true
                if calc[col] and col < self.width:
                    glVertex2i(col, row)

                # prep the current column for the next row
                if col + 1 < len(calc):
                    calc[col] ^= calc[col + 1]

        glEnd()

        glutSwapBuffers()


    def reshape(self, width, height):
        self.width = width
        self.height = height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
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
    sier = Sierpinski()
    sier.main()
