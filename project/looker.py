#! /usr/bin/python

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from datetime import datetime

import math
import random
import sys

ORG = [0.0, 0.0, 0.0]

XP = [1.0, 0.0, 0.0]
XN = [-1.0, 0.0, 0.0]

YP = [0.0, 1.0, 0.0]
YN = [0.0, -1.0, 0.0]

ZP = [0.0, 0.0, 1.0]
ZN = [0.0, 0.0, -1.0]


ROTATION = [0.0, 0.0]

WIDTH = 640
HEIGHT = 480

VIEW = [0.0, 0.0, 0.0]
PLAYER = [10.0, 11.7, 0.0]
POS_X = 10
POS_Y = 0
POS_Z = 10

CUBELIST = []

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


def draw_cube(x, y, z):
    d = 0.5

    glBegin(GL_QUADS)

    # top
    glVertex3f(x - d, y + d, z - d)
    glVertex3f(x - d, y + d, z + d)
    glVertex3f(x + d, y + d, z + d)
    glVertex3f(x + d, y + d, z - d)

    # bottom
    glVertex3f(x - d, y - d, z - d)
    glVertex3f(x + d, y - d, z - d)
    glVertex3f(x + d, y - d, z + d)
    glVertex3f(x - d, y - d, z + d)

    # left
    glVertex3f(x - d, y - d, z - d)
    glVertex3f(x - d, y - d, z + d)
    glVertex3f(x - d, y + d, z + d)
    glVertex3f(x - d, y + d, z - d)

    # right
    glVertex3f(x + d, y - d, z + d)
    glVertex3f(x + d, y - d, z - d)
    glVertex3f(x + d, y + d, z - d)
    glVertex3f(x + d, y + d, z + d)

    # front
    glVertex3f(x - d, y - d, z + d)
    glVertex3f(x + d, y - d, z + d)
    glVertex3f(x + d, y + d, z + d)
    glVertex3f(x - d, y + d, z + d)

    # back
    glVertex3f(x + d, y - d, z - d)
    glVertex3f(x - d, y - d, z - d)
    glVertex3f(x - d, y + d, z - d)
    glVertex3f(x + d, y + d, z - d)

    glEnd()


class Cube:
    def __init__(self, pos, c):
        self.pos = pos
        self.color = c

def set_cubelist():
    for z in range (-16, 16):
        for x in range(-16, 16):
            c = Cube((x, -1, z), 0.5 + random.random() / 2.0)
            CUBELIST.append(c)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, WIDTH / float(HEIGHT), 0.1, 60.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    gluLookAt(POS_X, 1.7, POS_Z,
              POS_X + 10 * math.cos(math.radians(ROTATION[0])),
              POS_Y + 10 * math.cos(math.radians(ROTATION[1])) + 1.7,
              POS_Z + 10 * math.sin(math.radians(ROTATION[0])),
              0, 1, 0)
    glColor3f(0.3, 0.8, 0.4)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    for c in CUBELIST:
        glColor3f(0.3, c.color, 0.4)
        draw_cube(*c.pos)

    glColor3f(1, 1, 1)

    draw_axes()
    glFlush()
    return

    if False:
        for x in range(-10, 10):
            for z in range(-10, 10):
                glColor3f(0.2, abs((x * z) / 100.0), 0.2)
                glBegin(GL_QUADS);
                glVertex3f(0, 0, 0)
                glVertex3f(10 * x, 0, 0)
                glVertex3f(10 * x, 0, 10 * z)
                glVertex3f(0, 0, 10 * z)
                glEnd()



def reshape(width, height):
    global WIDTH
    global HEIGHT

    WIDTH = width
    HEIGHT = height

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, width / float(height), 0.1, 60.0)

def keypress(key, x, y):
    global POS_X
    global POS_Z

    if key == b'w':
        POS_Z += 0.2 * math.sin(math.radians(ROTATION[0]))
        POS_X += 0.2 * math.cos(math.radians(ROTATION[0]))
    elif key == b's':
        POS_Z -= 0.2 * math.sin(math.radians(ROTATION[0]))
        POS_X -= 0.2 * math.cos(math.radians(ROTATION[0]))
    elif key == b'a':
        POS_Z += 0.2 * math.sin(math.radians(ROTATION[0] + 90))
        POS_X += 0.2 * math.cos(math.radians(ROTATION[0] + 90))
    elif key == b'd':
        POS_Z += 0.2 * math.sin(math.radians(ROTATION[0] - 90))
        POS_X += 0.2 * math.cos(math.radians(ROTATION[0] - 90))
    glutPostRedisplay()

def block_at_loc(x, y, z):
    x = int(x)
    y = int(y)
    z = int(z)
    return (x, y, z) in CUBELIST

TIME = datetime.now()

def idle():
    global TIME, POS_Y

    cur = datetime.now()
    diff = cur - TIME
    if diff.microseconds >= 20000:
        if not block_at_loc(POS_X, POS_Y - 1, POS_Z):
            POS_Y -= 0.1
        TIME = cur
        glutPostRedisplay()


def mouse(x, y):
    # When we look around, we want to point to a sphere around
    # the player's position. That way, when the mouse moves up,
    # down, left, and right, we show smooth motion.
    #
    # Conversion is as follows:
    #   x = r * sin(theta) * cos(phi)
    #   y = r * sin(theta) * sin(phi)
    #   z = cos(theta)
    # 
    # In our case, the radius of the sphere, r, doens't matter
    # because we're just using it as a direction to look.
    #

    x = x % 640
    y = y % 480
    ROTATION[0] = (x / 640.0) * 360.0
    ROTATION[1] = (y / 480.0) * 360.0 - 180.0

    glutPostRedisplay()

def main():
    set_cubelist()

    print("init")
    glutInit(sys.argv)
    print("init window pos")
    glutInitWindowPosition(200, 300)
    print("init window size")
    glutInitWindowSize(640, 480)
    print("init display mode")
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    print("create window")
    glutCreateWindow("Camera Analogy")
    print("set display func")
    glutDisplayFunc(display)
    print("set reshape func")
    glutReshapeFunc(reshape)
    print("set keypress func")
    glutKeyboardFunc(keypress)
    print("set mouse func")
    glutPassiveMotionFunc(mouse)
    print("set idle func")
    glutIdleFunc(idle)

    print("clear color")
    glClearColor(0.3, 0.4, 1.0, 1.0)

    print("main loop")
    glutMainLoop()
    print("done")


if __name__ == "__main__":
    main()
