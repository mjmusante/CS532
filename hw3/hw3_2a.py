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

        #
        # 2a)   Draw coordinate axes in different colors (position them
        #       in the center of your window).

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


        # now draw the polygon in white
        glColor3f(1.0, 1.0, 1.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_LINE_LOOP)
        for v in self.hexagon:
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
