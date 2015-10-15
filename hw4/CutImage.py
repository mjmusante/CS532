#! /usr/bin/python

from PIL import Image

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys


class CutImage:
    def __init__(self):
        self.img = bytearray()
        self.i_points = ()
        self.points = []
        self.avg = [0, 0]

    def plotPixel(self, x, y):
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        glVertex2i(x, y)
        glEnd()


    def display(self):
        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

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

        cval = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0),
                (1.0, 1.0, 1.0)]
        if len(self.points) > 0:
            glPointSize(8.0)
            glBegin(GL_POINTS)
            cnum = 0
            for i in self.points:
                glColor3f(*cval[cnum])
                glVertex2f(*i)
                cnum += 1
            glEnd()

            if len(self.points) == 4:
                glBegin(GL_LINE_LOOP)
                for i in self.points:
                    glVertex2f(*i)
                glEnd()

        glColor3f(1.0, 1.0, 1.0)
        glutSwapBuffers()


    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        self.width = width
        self.height = height

        if width > height:
            self.ysize = 1.0
            self.xsize = 1.0 * width / height
        else:
            self.xsize = 1.0
            self.ysize = 1.0 * height / width
        gluOrtho2D(-self.xsize, self.xsize, self.ysize, -self.ysize)


    def mouse(self, button, state, x, y):
        if len(self.points) == 4:
            return

        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                point = (x, y)
                if point not in self.i_points:
                    self.i_points += (point,)
                    xpoint = self.xsize * (2.0 * x / self.width - 1.0)
                    ypoint = self.ysize * (2.0 * y / self.height - 1.0)

                    # ensure that the point is within the image
                    if xpoint < -1.0 or xpoint > 1.0 or \
                       ypoint < -1.0 or ypoint > 1.0:
                        return

                    # add the point to the points list
                    self.points.append((xpoint, ypoint))

                    self.avg[0] += xpoint
                    self.avg[1] += ypoint

                    if len(self.points) == 4:
                        self.avg[0] /= 4.0
                        self.avg[1] /= 4.0

                        def det(i, j):
                            a = self.points[i][0] - self.avg[0]
                            b = self.points[i][1] - self.avg[1]
                            c = self.points[j][0] - self.avg[0]
                            d = self.points[j][1] - self.avg[1]
                            return a * d - b * c

                        def slope_intercept(i, j):
                            a = self.points[i][0]
                            b = self.points[i][1]
                            c = self.points[j][0]
                            d = self.points[j][1]
                            slope = (d - b) / (c - a)
                            intercept = b - slope * a
                            return (slope, intercept)


                        self.det = [0, 0, 0, 0]
                        self.si = ()
                        for i in range(0, 4):
                            np = (i + 1) % 4
                            self.det[i] = det(i, np)
                            if self.det[i] > 0.0:
                                x = self.points[i]
                                self.points[i] = self.points[np]
                                self.points[np] = x
                                self.det[i] = det(i, np)
                            self.si += ((slope_intercept(i, np)),)
                            print("%7.4f %7.4f" % (self.si[i]))

                    glutPostRedisplay()

    def main(self):
        glutInit(sys.argv)
        glutInitWindowPosition(200, 300)
        glutInitWindowSize(640, 480)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutCreateWindow("GLUT Window")
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutMouseFunc(self.mouse)

        glClearColor(0.2, 0.2, 0.2, 1.0)

        i = Image.open("../images/Spring.bmp")
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
    x = CutImage()
    x.main()
