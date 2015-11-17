#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys

ORG = [0.0, 0.0, 0.0]

XP = [1.0, 0.0, 0.0]
XN = [-1.0, 0.0, 0.0]

YP = [0.0, 1.0, 0.0]
YN = [0.0, -1.0, 0.0]

ZP = [0.0, 0.0, 1.0]
ZN = [0.0, 0.0, -1.0]

def draw_axes():
    glLineWidth(2.0)

    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)    # x-axis is red
    glVertex3fv(ORG)
    glVertex3fv(XP)
    glColor3f(0.0, 1.0, 0.0)    # y-axis is green
    glVertex3fv(ORG)
    glVertex3fv(YP)
    glColor3f(0.0, 0.0, 1.0)    # z-axis is lue
    glVertex3fv(ORG)
    glVertex3fv(ZP)
    glEnd()




def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(0.5, 0.7, 1.0)
    gluLookAt(0.0, 3.0, 5.0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0)

    draw_axes()

    method = 0

    if method == 0:
        # 3d transform by using ogl functions
        glTranslatef(0.0, 0.5, 1.0)
        glRotatef(45.0, 0.0, 1.0, 0.0)
    elif method == 1:
        # 3d transform by using transform matrix
        print("method 1")
    else:
        # 3d transform by coded matrix multiplication
        glPushMatrix()
        # insert code ehere
        glPopMatrix()

    glColor3f(0.5, 0.7, 1.0)
    glutWireTeapot(1.0)

    glFlush()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.0, 1.0, -1.0, 1.0, 3.0, 60.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(640, 480)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutCreateWindow("Camera Analogy")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
