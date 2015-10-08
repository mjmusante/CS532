#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys

def plotPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()


def DrawLineGL(p1, p2, width):
    glColor3f(1.0, 0.5, 0.1)
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2iv(p1)
    glVertex2iv(p2)
    glEnd()


def Triangle(v1, v2, v3):
    glBegin(GL_TRIANGLES)
    glVertex2iv(v1)
    glVertex2iv(v2)
    glVertex2iv(v3)
    glEnd()


def TriangleStrip(v1, v2, v3, v4, v5):
    glBegin(GL_TRIANGLE_STRIP)
    glVertex2iv(v1)
    glVertex2iv(v2)
    glVertex2iv(v3)
    glVertex2iv(v4)
    glVertex2iv(v5)
    glEnd()


def TriangleFan(v1, v2, v3, v4, v5):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2iv(v1)
    glVertex2iv(v2)
    glVertex2iv(v3)
    glVertex2iv(v4)
    glVertex2iv(v5)
    glEnd()


def Quad(v1, v2, v3, v4):
    glBegin(GL_QUADS)
    glVertex2iv(v1)
    glVertex2iv(v2)
    glVertex2iv(v3)
    glVertex2iv(v4)
    glEnd()


def QuadStrip(v1, v2, v3, v4, v5, v6):
    glBegin(GL_QUAD_STRIP)
    glVertex2iv(v1)
    glVertex2iv(v2)
    glVertex2iv(v3)
    glVertex2iv(v4)
    glVertex2iv(v5)
    glVertex2iv(v6)
    glEnd()



def Polygon(v1, v2, v3, v4, v5, v6):
    glBegin(GL_POLYGON)
    glVertex2iv(v1)
    glVertex2iv(v2)
    glVertex2iv(v3)
    glVertex2iv(v4)
    glVertex2iv(v5)
    glVertex2iv(v6)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.4, 1.0, 0.0)

    glShadeModel(GL_FLAT)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLineWidth(3)

    v1 = (100, 100)
    v2 = (150, 150)
    v3 = (100, 200)
    v4 = (150, 200)
    v5 = (150, 250)
    v6 = (150, 300)
    v7 = (200, 350)
    v8 = (300, 150)

    primitive = 5

    if primitive == 0:
        Triangle(v1, v2, v3)
    elif primitive == 1:
        TriangleStrip(v1, v2, v3, v4, v5)
    elif primitive == 2:
        TriangleFan(v1, v2, v3, v4, v5)
    elif primitive == 3:
        Quad(v1, v2, v5, v3)
    elif primitive == 4:
        QuadStrip(v1, v2, v3, v5, v6, v7)
    elif primitive == 5:
        Polygon(v1, v2, v3, v6, v7, v8)

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-width, width, height, -height)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(640, 480)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("Draw 2D Pimitives")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
