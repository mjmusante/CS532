#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys

def polygon_fill():

    # A - Choose polygon shading
    glShadeModel(GL_FLAT)
    # glShadeModel(GL_SMOOTH)

    # B - Polygon rasterisation mode
    # glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glPolygonMode(GL_BACK, GL_FILL)

    glBegin(GL_POLYGON)
    glColor3f(1.0, 0.5, 0.1)    # Fill color orange
    glVertex2i(10, 10)
    glColor3f(0.0, 1.0, 0.0)    # green vertex
    glVertex2i(100, 30)
    glColor3f(0.0, 0.0, 1.0)    # blue vertex
    glVertex2i(250, 100)
    glVertex2i(300, 200)
    glColor3f(1.0, 0.0, 0.0)    # red vertex
    glVertex2i(100, 250)
    glVertex2i(10, 100)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    polygon_fill()
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
    glutCreateWindow("Polygon GL")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glClearColor(0.2, 0.2, 0.2, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
