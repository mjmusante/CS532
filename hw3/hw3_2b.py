#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math
import sys

class MainDisplay:
    def __init__(self):
        self.my_view = 400
        self.hexagon = (
                ( 100,   0),
                (  50, -87),
                ( -50, -87),
                (-100,   0),
                ( -50,  87),
                (  50,  87),
        )


    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # x-axis in red
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex2i(-self.my_view, 0)
        glVertex2i(self.my_view, 0)
        glEnd()

        # y-axis in green
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        glVertex2i(0, -self.my_view)
        glVertex2i(0, self.my_view)
        glEnd()


        # draw original image in faint blue
        glColor3f(0.25, 0.25, 0.5)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_LINE_LOOP)
        for v in self.hexagon:
            glVertex2i(*v)
        glEnd()

        #
        # 2b)   Translate your polygon along y axis for 1.5 times the
        #       figure's y size.
        #
        # The figure's y-size is 200 pixels, so 1.5 of that is 300. This
        # results in a translation matrix of
        #
        #   +-           -+
        #   | 1    0    0 |
        #   | 0    1  300 |
        #   | 0    0    1 |
        #   +-           -+

        transform = (
                (1, 0,   0),
                (0, 1, 300),
                (0, 0,   1),
            )

        # Perform the transform
        result = ()
        for v in self.hexagon:
            col = [0, 0, 0]
            i = 0
            for t in transform:
                col[i] += int(round(v[0] * t[0] + v[1] * t[1] + t[2]))
                i += 1
            result += ((col[0], col[1]),)

        # draw transformed image in white
        glColor3f(1.0, 1.0, 1.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_LINE_LOOP)
        for v in result:
            glVertex2i(*v)
        glEnd()



        
        glutSwapBuffers()


    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if width > height:
            boxh = self.my_view
            boxw = self.my_view * width / height
        else:
            boxh = self.my_view * height / width
            boxw = self.my_view

        gluOrtho2D(-boxw, boxw, boxh, -boxh)

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
    md = MainDisplay()
    md.main()
