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
JUMPTIME = 0
LASTTIME = 0

FORWARD = False
BACKWARD = False
MOVE_LEFT = False
MOVE_RIGHT = False

LOOK_X, LOOK_Y, LOOK_Z = (0, 0, 0)

CUBELIST = {}
CUBELINES = False
pCUBELINES = False
DOTS = []

def draw_reticle():
    global WIDTH, HEIGHT

    glLineWidth(2.0)
    glBegin(GL_LINES)

    vert_top = HEIGHT / 2 - 10
    vert_bot = HEIGHT / 2 + 10

    horiz_left = WIDTH / 2 - 10
    horiz_right = WIDTH / 2 + 10

    glVertex2f(WIDTH / 2, vert_top)
    glVertex2f(WIDTH / 2, vert_bot)

    glVertex2f(horiz_left, HEIGHT / 2)
    glVertex2f(horiz_right, HEIGHT / 2)

    glEnd()


def draw_cubelines(x, y, z):
        glBegin(GL_LINE_LOOP)
        glVertex3f(x, y - 1, z)
        glVertex3f(x + 1, y - 1, z)
        glVertex3f(x + 1, y, z)
        glVertex3f(x, y, z)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glVertex3f(x, y - 1, z + 1)
        glVertex3f(x + 1, y - 1, z + 1)
        glVertex3f(x + 1, y, z + 1)
        glVertex3f(x, y, z + 1)
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(x, y, z)
        glVertex3f(x, y, z + 1)
        glVertex3f(x + 1, y, z)
        glVertex3f(x + 1, y, z + 1)
        glEnd()

def draw_cube(x, y, z):

    # top
    if not (x, y+1, z) in CUBELIST:
        TEX_TOP.draw([(x    , y, z    ), (x    , y, z + 1),
                      (x + 1, y, z + 1), (x + 1, y, z    )])

    # bottom
    if not (x, y-1, z) in CUBELIST:
        TEX_BOT.draw([(x    , y - 1, z    ), (x + 1, y - 1, z    ),
                      (x + 1, y - 1, z + 1), (x    , y - 1, z + 1)])

    # left
    if not (x-1, y, z) in CUBELIST:
        TEX_SIDE.draw([(x    , y - 1, z    ), (x    , y - 1, z + 1),
                       (x    , y    , z + 1), (x    , y    , z    )])

    # right
    if not (x+1, y, z) in CUBELIST:
        TEX_SIDE.draw([(x + 1, y - 1, z + 1), (x + 1, y - 1, z    ),
                       (x + 1, y    , z    ), (x + 1, y    , z + 1)])

    # front
    if not (x, y, z+1) in CUBELIST:
        TEX_SIDE.draw([(x    , y - 1, z + 1), (x + 1, y - 1, z + 1),
                       (x + 1, y    , z + 1), (x    , y    , z + 1)])

    # back
    if not (x, y, z-1) in CUBELIST:
        TEX_SIDE.draw([(x + 1, y - 1, z    ), (x    , y - 1, z    ),
                       (x    , y    , z    ), (x + 1, y    , z    )])


class Cube:
    def __init__(self, pos, c):
        self.pos = pos
        self.color = c

def set_cubelist():
    for z in range (-16, 16):
        for x in range(-16, 16):
            for y in range(-4, 1):
                pos = (x, y, z)
                CUBELIST[pos] = 1
    CUBELIST[(10, 1, 10)] = 1
    CUBELIST[(10, 2, 10)] = 1


def display():
    global POS_X, POS_Y, POS_Z
    global LOOK_X, LOOK_Y, LOOK_Z
    global CUBELIST, CUBELINES, DOTS

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 3D Drawing: using gluPerspective
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, WIDTH / float(HEIGHT), 0.1, 60.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glDepthFunc(GL_LESS)
    gluLookAt(POS_X, POS_Y + 1.7, POS_Z,
              POS_X + LOOK_X, POS_Y + 1.7 + LOOK_Y, POS_Z + LOOK_Z,
              0, 1, 0)

    glColor3f(1, 1, 1)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    for c in CUBELIST:
        draw_cube(*c)

    if CUBELINES:
        glColor3f(0, 0, 0)
        glLineWidth(5.0)
        draw_cubelines(*CUBELINES)

    if len(DOTS) > 0:
        glBegin(GL_POINTS)
        for d in DOTS:
            glVertex3f(*d)
        glEnd()
    # 2D Drawing: using gluOrtho2D
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)
    gluOrtho2D(0, WIDTH, HEIGHT, 0);

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3f(1, 1, 1)
    draw_reticle()
        
    glFlush()
    return




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
    global MOVE_LEFT, MOVE_RIGHT

    new_x = POS_X
    new_z = POS_Z

    if key == b'w':
        FORWARD = True
    elif key == b's':
        BACKWARD = True
    elif key == b'a':
        MOVE_LEFT = True
    elif key == b'd':
        MOVE_RIGHT = True
    elif key == b' ':
        JUMP = True
    elif key == b'\x1b':
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

def keyup(key, x, y):
    global FORWARD, BACKWARD
    global MOVE_LEFT, MOVE_RIGHT
    global JUMP

    if key == b'w':
        FORWARD = False
    elif key == b's':
        BACKWARD = False
    elif key == b'a':
        MOVE_LEFT = False
    elif key == b'd':
        MOVE_RIGHT = False
    elif key == b' ':
        JUMP = False

def block_at_pos(x, y, z):
    x = int(x)
    y = int(y)
    z = int(z)
    return (x, y, z) in CUBELIST

def timer(val):
    global FORWARD, BACKWARD, ROTATION
    global MOVE_LEFT, MOVE_RIGHT
    global POS_X, POS_Y, POS_Z
    global LOOK_X, LOOK_Y
    global LOOK_X_90, LOOK_Z_90
    global JUMP, JUMPING, JUMPTIME, JUMPBASE
    global CUBELINES, pCUBELINES, DOTS
    global LASTTIME

    glutTimerFunc(33, timer, 0)
    now = datetime.now()
    diff = now - LASTTIME
    LASTTIME = now

    new_x, new_y, new_z = (POS_X, POS_Y, POS_Z)

    dist = 4.0 * (diff.seconds * 1000.0 + diff.microseconds / 1000.0) / 1000.0
    if FORWARD:
        new_x += dist * LOOK_X
        new_z += dist * LOOK_Z
    if BACKWARD:
        new_x -= dist * LOOK_X
        new_z -= dist * LOOK_Z
    if MOVE_LEFT:
        new_x += dist * LOOK_X_90
        new_z += dist * LOOK_Z_90
    if MOVE_RIGHT:
        new_x -= dist * LOOK_X_90
        new_z -= dist * LOOK_Z_90

    CUBELINES = False
    DOTS = []
    i = 0.0
    while i < 5.0:
        i += 0.1
        x = POS_X + LOOK_X * i
        y = 1.7 + POS_Y + LOOK_Y * i
        z = POS_Z + LOOK_Z * i
        # DOTS.append((x, y, z),)
        foo = (int(x + 0.5), int(y + 0.5), int(z + 0.5))
        if block_at_pos(*foo):
            CUBELINES = foo
            break
        else:
            pCUBELINES = foo

    if JUMPING:
        dur = datetime.now() - JUMPTIME
        ms = dur.seconds * 10**3 + dur.microseconds / 10**3
        if ms > 800:
            JUMPING = False
        else:
            new_y = JUMPBASE + 2 * math.sin(math.radians(180.0 * ms / 800))
    elif JUMP:
        JUMPING = True
        JUMPTIME = datetime.now()
        JUMPBASE = POS_Y
    elif not block_at_pos(POS_X, POS_Y - 1, POS_Z) or \
            POS_Y > int(POS_Y) + 0.25:
        new_y -= 0.2

    update_position(new_x, new_y, new_z)
    glutPostRedisplay()


def mouse(x, y):
    global LOOK_X, LOOK_Y, LOOK_Z
    global LOOK_X_90
    global LOOK_Z_90
    global WIDTH, HEIGHT

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

    x = float(x % WIDTH)
    y = float(y % HEIGHT)
    ROTATION[0] = 180.0 - (x / WIDTH) * 180.0
    ROTATION[1] = 180.0 - (y / HEIGHT) * 360.0

    phi = math.radians(ROTATION[0])
    phi90 = math.radians(ROTATION[0] + 90)
    theta = math.radians(ROTATION[1])
    LOOK_X =  math.sin(phi) * math.cos(theta)
    LOOK_X_90 =  math.sin(phi90) * math.cos(theta)
    LOOK_Y =  math.sin(phi) * math.sin(theta)
    LOOK_Z =  math.cos(phi)
    LOOK_Z_90 =  math.cos(phi90)

def clicker(button, state, x, y):
    global CUBELINES

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if CUBELINES:
            if CUBELINES in CUBELIST:
                del CUBELIST[CUBELINES]
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if CUBELINES:
            if pCUBELINES not in CUBELIST:
                CUBELIST[pCUBELINES] = 1

def main():
    global WIN, TEX_TOP, TEX_BOT, TEX_SIDE
    global LASTTIME

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
    glutMouseFunc(clicker)
    LASTTIME = datetime.now()
    glutTimerFunc(50, timer, 0)
    # glutIdleFunc(idle)

    TEX_TOP = Texture()
    TEX_TOP.load("grass-top-16x16.jpg")

    TEX_BOT = Texture()
    TEX_BOT.load("grass-bot-16x16.jpg")

    TEX_SIDE = Texture()
    TEX_SIDE.load("grass-side-16x16.jpg")

    glClearColor(0.3, 0.4, 1.0, 1.0)

    glutMainLoop()


if __name__ == "__main__":
    main()
