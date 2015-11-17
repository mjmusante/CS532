#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0.0, 3.0, 5.0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0)

#    glColor3f(0.2, 1.0, 0.3)
#    glBegin(GL_QUADS)
#    glVertex3f(-30.0, 0.0, -30.0)
#    glVertex3f(-30.0, 0.0,  30.0)
#    glVertex3f( 30.0, 0.0,  30.0)
#    glVertex3f( 30.0, 0.0, -30.0)
#    glEnd()

    glFlush()
    # glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # gluOrtho2D(0, width, height, 0)
    glFrustum(-1.0, 1.0, -1.0, 1.0, 3.0, 60.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(640, 480)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("GLUT Window")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glClearColor(0.1, 0.1, 1.0, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
