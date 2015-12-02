#! /usr/bin/python

from __future__ import print_function

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from datetime import datetime

from util.texture import Texture

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

TEX_TOP = False
TEX_BOT = False
TEX_SIDE = False

ROTATION = [0.0, 0.0]

WIDTH = 640
HEIGHT = 480

VIEW = [0.0, 0.0, 0.0]
PLAYER = [10.0, 11.7, 0.0]
POS_X = 0
POS_Y = 0
POS_Z = 0
JUMP = False
JUMPING = False
JUMPLOC = 0
JUMPDEG = 0

FORWARD = False
BACKWARD = False

CUBELIST = {}

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


    # top
    if not (x, y+1, z) in CUBELIST:
        TEX_TOP.draw([(x - d, y + d, z - d), (x - d, y + d, z + d),
                      (x + d, y + d, z + d), (x + d, y + d, z - d)])

    # bottom
    if not (x, y-1, z) in CUBELIST:
        TEX_BOT.draw([(x - d, y - d, z - d), (x + d, y - d, z - d),
                      (x + d, y - d, z + d), (x - d, y - d, z + d)])

    # left
    if not (x-1, y, z) in CUBELIST:
        TEX_SIDE.draw([(x - d, y - d, z - d), (x - d, y - d, z + d),
                       (x - d, y + d, z + d), (x - d, y + d, z - d)])

    # right
    if not (x+1, y, z) in CUBELIST:
        TEX_SIDE.draw([(x + d, y - d, z + d), (x + d, y - d, z - d),
                       (x + d, y + d, z - d), (x + d, y + d, z + d)])

    # front
    if not (x, y, z+1) in CUBELIST:
        TEX_SIDE.draw([(x - d, y - d, z + d), (x + d, y - d, z + d),
                       (x + d, y + d, z + d), (x - d, y + d, z + d)])

    # back
    if not (x, y, z-1) in CUBELIST:
        TEX_SIDE.draw([(x + d, y - d, z - d), (x - d, y - d, z - d),
                       (x - d, y + d, z - d), (x + d, y + d, z - d)])


class Cube:
    def __init__(self, pos, c):
        self.pos = pos
        self.color = c

def set_cubelist():
    blah = ""
    for z in range (-16, 16):
        for x in range(-16, 16):
            for y in range(-4, 1):
                pos = (x, y, z)
                CUBELIST[pos] = 1
    print(blah)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, WIDTH / float(HEIGHT), 0.1, 60.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glDepthFunc(GL_LESS)
    gluLookAt(POS_X, POS_Y + 1.7, POS_Z,
              POS_X + 10 * math.cos(math.radians(ROTATION[0])),
              POS_Y + 10 * math.cos(math.radians(ROTATION[1])) + 1.7,
              POS_Z + 10 * math.sin(math.radians(ROTATION[0])),
              0, 1, 0)

    glColor3f(1, 1, 1)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    for c in CUBELIST:
        draw_cube(*c)


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
    global POS_X, POS_Y, POS_Z
    global JUMP
    global WIN
    global FORWARD, BACKWARD

    new_x = POS_X
    new_z = POS_Z

    if key == b'w':
        # new_z += 0.2 * math.sin(math.radians(ROTATION[0]))
        # new_x += 0.2 * math.cos(math.radians(ROTATION[0]))
        print("forward start")
        FORWARD = True
    elif key == b's':
        # new_z -= 0.2 * math.sin(math.radians(ROTATION[0]))
        # new_x -= 0.2 * math.cos(math.radians(ROTATION[0]))
        print("backward start")
        BACKWARD = True
    elif key == b'a':
        new_z += 0.2 * math.sin(math.radians(ROTATION[0] + 90))
        new_x += 0.2 * math.cos(math.radians(ROTATION[0] + 90))
    elif key == b'd':
        new_z += 0.2 * math.sin(math.radians(ROTATION[0] - 90))
        new_x += 0.2 * math.cos(math.radians(ROTATION[0] - 90))
    elif key == b' ':
        JUMP = True
    elif key == "\x1b":
        glutDestroyWindow(WIN)
        sys.exit(0)
    else:
        print(key)


def update_position(new_x, new_y, new_z):
    global POS_X, POS_Y, POS_Z

    if not block_at_pos(new_x, new_y + 1, new_z) and \
       not block_at_pos(new_x, new_y + 2, new_z):
        POS_X = new_x
        POS_Y = new_y
        POS_Z = new_z
        redisp = True

    return redisp

def keyup(key, x, y):
    global FORWARD, BACKWARD
    if key == b'w':
        FORWARD = False
        print('forward end')
    elif key == b's':
        BACKWARD = False
        print('backward end')

def block_at_pos(x, y, z):
    x = int(x)
    y = int(y)
    z = int(z)
    return (x, y, z) in CUBELIST

def timer(val):
    glutTimerFunc(33, timer, 0)

    global FORWARD, BACKWARD, ROTATION
    global POS_X, POS_Y, POS_Z

    new_x, new_y, new_z = (POS_X, POS_Y, POS_Z)

    if FORWARD:
        new_z += 0.2 * math.sin(math.radians(ROTATION[0]))
        new_x += 0.2 * math.cos(math.radians(ROTATION[0]))
    if BACKWARD:
        new_z -= 0.2 * math.sin(math.radians(ROTATION[0]))
        new_x -= 0.2 * math.cos(math.radians(ROTATION[0]))

    if not block_at_pos(POS_X, POS_Y - 1, POS_Z) or \
            POS_Y > int(POS_Y) + 0.25:
        new_y -= 0.2
    
    if update_position(new_x, new_y, new_z):
        glutPostRedisplay()



TIME = datetime.now()

def idle():
    global TIME, POS_Y
    global JUMP, JUMPING, JUMPDEG, JUMPLOC

    cur = datetime.now()
    diff = cur - TIME
    if diff.microseconds >= 50000:
        TIME = cur
        redisp = False

        if not block_at_pos(POS_X, POS_Y - 1, POS_Z) or \
                POS_Y > int(POS_Y) + 0.25:
            POS_Y -= 0.25
            redisp = True

        if JUMPING:
            JUMPDEG += 10
            if JUMPDEG < 180:
                new_y = JUMPLOC + 2 * math.sin(math.radians(JUMPDEG))
            else:
                new_y = JUMPLOC
                JUMPING = False

            if block_at_pos(POS_X, new_y, POS_Z):
                new_y = int(new_y) + 1
                JUMPING = False

            POS_Y = new_y
            JUMP = False
        elif JUMP:
            JUMPING = True
            JUMPDEG = 0
            JUMPLOC = POS_Y
            JUMP = False

        if redisp:
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
    global WIN, TEX_TOP, TEX_BOT, TEX_SIDE

    set_cubelist()

    glutInit(sys.argv)
    glutInitWindowPosition(200, 300)
    glutInitWindowSize(640, 480)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    WIN = glutCreateWindow("Camera Analogy")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutSetKeyRepeat(GLUT_KEY_REPEAT_OFF);
    glutKeyboardFunc(keypress)
    glutKeyboardUpFunc(keyup)
    glutPassiveMotionFunc(mouse)
    glutTimerFunc(50, timer, 0)
    # glutIdleFunc(idle)

    TEX_TOP = Texture()
    TEX_TOP.load("grass-top.jpg")

    TEX_BOT = Texture()
    TEX_BOT.load("grass-bottom.jpg")

    TEX_SIDE = Texture()
    TEX_SIDE.load("grass-side.jpg")

    glClearColor(0.3, 0.4, 1.0, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
