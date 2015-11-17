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

useFrustum = 1

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
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(0.5, 0.7, 1.0)
    gluLookAt(0.0, 2.0, 5.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0)
    # glutWireCube(1.0)
    glutWireTeapot(1.0)

    draw_axes()
    glFlush()


def reshape(width, height):
    w = width
    h = height
    if w > height:
        w = height
    elif h > width:
        h = width

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if useFrustum:
        glFrustum(-1.0, 1.0, -1.0, 1.0, 3.0, 6.0)
    else:
        glOrtho(-2.0, 2.0, -2.0, 2.0, 3.0, 6.0)
    glMatrixMode(GL_MODELVIEW)


def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            useFrustum = 1
        else:
            useFrustum = 0

        glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(640, 480)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutCreateWindow("Camera Analogy")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
