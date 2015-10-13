#! /usr/bin/python

from PIL import Image

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys


class Blah:
    def __init__(self):
        self.img = bytearray()

    def plotPixel(self, x, y):
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        glVertex2i(x, y)
        glEnd()


    def display(self):
        # glClearDepth(1)
        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)

        glTexCoord2f(0.0, 0.0)
        glVertex2f(-1.0, 1.0)

        glTexCoord2f(0.0, 1.0)
        glVertex2f(-1.0, -1.0)

        glTexCoord2f(1.0, 1.0)
        glVertex2f(1.0, -1.0)

        glTexCoord2f(1.0, 0.0)
        glVertex2f(1.0, 1.0)

        glEnd()
        glDisable(GL_TEXTURE_2D)

        self.plotPixel(100, 200)

        glutSwapBuffers()


    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluOrtho2D(0, 10, 10, 0)

        glMatrixMode(GL_PROJECTION)


    def main(self):
        glutInit(sys.argv)
        glutInitWindowPosition(200, 300)
        glutInitWindowSize(640, 480)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutCreateWindow("GLUT Window")
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)

        glClearColor(0.2, 0.2, 0.2, 1.0)

        i = Image.open("Spring.bmp")
        foo = i.getdata()
        for x in foo:
            self.img.append(x[0])
            self.img.append(x[1])
            self.img.append(x[2])

        self.texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, i.size[0], i.size[1],
                0, GL_RGB, GL_UNSIGNED_BYTE, self.img)


        glutMainLoop()


if __name__ == "__main__":
    x = Blah()
    x.main()
