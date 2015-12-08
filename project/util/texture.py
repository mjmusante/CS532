#! /usr/bin/python

from PIL import Image

from OpenGL.GL import *

import sys

class Texture:
    def __init__(self):
        self.loaded = False

    def load(self, path):
        try:
            i = Image.open(path)
        except:
            print("could not find %s" % (path))
            sys.exit(0)

        self.width = i.size[0]
        self.height = i.size[1]

        self.img = bytearray()
        for d in i.getdata():
            self.img.append(d[0])
            self.img.append(d[1])
            self.img.append(d[2])

        self.texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0,
                     GL_RGB, GL_UNSIGNED_BYTE, self.img)

    def draw(self, vertex):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(*vertex[0])

        glTexCoord2f(0.0, 1.0)
        glVertex3f(*vertex[1])

        glTexCoord2f(0.0, 0.0)
        glVertex3f(*vertex[2])

        glTexCoord2f(1.0, 0.0)
        glVertex3f(*vertex[3])

        glEnd()
