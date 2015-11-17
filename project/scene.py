#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math
import sys

ORG = [0.0, 0.0, 0.0]

XP = [1.0, 0.0, 0.0]
XN = [-1.0, 0.0, 0.0]

YP = [0.0, 1.0, 0.0]
YN = [0.0, -1.0, 0.0]

ZP = [0.0, 0.0, 1.0]
ZN = [0.0, 0.0, -1.0]


VIEW = [10.0, 0.0, 10.0]
PLAYER = [0.0, 1.7, 0.0]

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
    gluLookAt(PLAYER[0], PLAYER[1], PLAYER[2],
            VIEW[0], VIEW[1], VIEW[2], 0.0, 10.0, 0.0)

    draw_axes()

    glColor3f(0.5, 0.7, 0.4)
    glBegin(GL_QUADS)
    glVertex3f(-10.0, 0.0, -10.0)
    glVertex3f(-10.0, 0.0,  10.0)
    glVertex3f( 10.0, 0.0,  10.0)
    glVertex3f( 10.0, 0.0, -10.0)
    glEnd()
    # glutWireTeapot(1.0)

    glFlush()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.0, 1.0, -1.0, 1.0, 3.0, 60.0)
    glMatrixMode(GL_MODELVIEW)


def mouse(x, y):
    yr = (y / 480.0) * 180.0 - 90.0
    xr = (x / 640.0) * 360.0
    m = math.cos(math.radians(yr))
    # VIEW[0] = math.cos(math.radians(xr - 90)) * m
    VIEW[1] = math.sin(math.radians(yr))
    # VIEW[2] = math.sin(math.radians(xr - 90)) * m
    # print("(%f %f %f)" % (VIEW[0], VIEW[1], VIEW[2]))
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(640, 480)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutCreateWindow("Camera Analogy")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutPassiveMotionFunc(mouse)

    glClearColor(0.3, 0.4, 1.0, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
