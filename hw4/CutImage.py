#! /usr/bin/python

from __future__ import print_function

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
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        self.show_crop = False
        self.img_ratio = 1.0
        self.do_greyscale = True

    def convertPoint(self, x, y):
        rx = float(self.tx) / self.width
        ry = float(self.ty) / self.height
        mx = rx * self.width / 2.0
        my = ry * self.height / 2.0
        xpoint = (x - mx) / mx
        ypoint = (y - my) / my
        return (xpoint, ypoint)


    def offsetPoint(self, x, y):
        return (xpoint, ypoint)

    def display(self):
        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)

        if self.show_crop:
            glBindTexture(GL_TEXTURE_2D, self.cropped)
            vertex1 = self.convertPoint(self.min_x, self.min_y)
            vertex2 = self.convertPoint(self.min_x, self.max_y)
            vertex3 = self.convertPoint(self.max_x, self.max_y)
            vertex4 = self.convertPoint(self.max_x, self.min_y)
        else:
            glBindTexture(GL_TEXTURE_2D, self.texture)
            vertex1 = (-1.0,  1.0)
            vertex2 = (-1.0, -1.0)
            vertex3 = ( 1.0, -1.0)
            vertex4 = ( 1.0,  1.0)

        glBegin(GL_QUADS)

        glTexCoord2f(0.0, 0.0)
        glVertex2f(*vertex1)

        glTexCoord2f(0.0, 1.0)
        glVertex2f(*vertex2)

        glTexCoord2f(1.0, 1.0)
        glVertex2f(*vertex3)

        glTexCoord2f(1.0, 0.0)
        glVertex2f(*vertex4)

        glEnd()
        glDisable(GL_TEXTURE_2D)

        #
        # Draw the points in this order: red, green, blue, white.
        # This allows us to visually distinguish each point, and
        # determine that the "reorder" algorithm is actually
        # working to sort the points anticlockwise.
        #
        cval = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0),
                (1.0, 1.0, 1.0)]
        if len(self.points) > 0:
            glPointSize(8.0)
            glBegin(GL_POINTS)
            cnum = 0
            for i in self.points:
                glColor3f(*cval[cnum])
                glVertex2f(*self.convertPoint(*i))
                cnum += 1
            glEnd()

            if len(self.points) == 4:
                glBegin(GL_LINE_LOOP)
                for i in self.points:
                    glVertex2f(*self.convertPoint(*i))
                glEnd()

        glColor3f(1.0, 1.0, 1.0)

        # show the min & max for the quad
        if self.min_x:
            glBegin(GL_LINE_LOOP)
            glVertex2f(*self.convertPoint(self.min_x, self.min_y))
            glVertex2f(*self.convertPoint(self.min_x, self.max_y))
            glVertex2f(*self.convertPoint(self.max_x, self.max_y))
            glVertex2f(*self.convertPoint(self.max_x, self.min_y))
            glEnd()

        glutSwapBuffers()


    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        self.width = width
        self.height = height

        if width * self.img_ratio > height:
            self.ysize = 1.0
            self.xsize = self.img_ratio * width / height
            self.xoffset = (width - self.tx) / 2
            self.yoffset = 0
        else:
            self.xsize = 1.0
            self.ysize = 1.0 * height / (width * self.img_ratio)
            self.xoffset = 0
            self.yoffset = (height - self.ty) / 2
        gluOrtho2D(-self.xsize, self.xsize, self.ysize, -self.ysize)


    def mouse(self, button, state, x, y):
        if len(self.points) == 4:
            return

        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                x -= self.xoffset
                y -= self.yoffset
                point = (x, y)

                # if two clicks are colocated, ignore the second one
                if point in self.i_points:
                    return

                self.i_points += (point,)

                # ensure that the point is within the image
                (cx, cy) = self.convertPoint(x, y)
                if cx < -1.0 or cx > 1.0 or cy < -1.0 or cy > 1.0:
                    return

                # add the point to the points list

                self.points.append(point)
 
                self.avg[0] += x
                self.avg[1] += y

                # self.points = [(0, 0), (1, 7), (8, 8), (7, 1)]
                # self.avg[0] = 0 + 1 + 8 + 7
                # self.avg[1] = 0 + 7 + 8 + 1

                if len(self.points) == 4:
                    self.select_inside()

                glutPostRedisplay()

    def crop_image(self):
        for v in range(self.min_y, self.max_y + 1):
            for h in range(self.min_x, self.max_x + 1):

                inside = True
                for seg in range(0, 4):
                    nseg = (seg + 1) % 4
                    (h1, h2) = (self.points[seg][0], self.points[nseg][0])
                    (v1, v2) = (self.points[seg][1], self.points[nseg][1])
                    if self.slope[seg] != None:
                        yL = self.slope[seg] * h + self.intercept[seg]

                        def pointInQuad(h1, v1, h2, v2, Hpix, yL, Vpix):
                            # copied directly from Select_Inside.m
                            if h2 > h1:
                                if yL < Vpix:
                                    return False
                            elif h2 < h1:
                                if yL > Vpix:
                                    return False
                            else:
                                if Hpix < h2 and v2 > v1:
                                    return False
                                if Hpix > h2 and v2 < v1:
                                    return False
                            return True

                        if not pointInQuad(h1, v1, h2, v2, h, yL, v):
                            inside = False
                            break

                if self.do_greyscale:
                    if inside:
                        start = 3 * self.tx * (self.ty - v) + 3 * h
                        rval = self.img[start]
                        gval = self.img[start + 1]
                        bval = self.img[start + 2]

                        self.crop.append(int(0.2989 * rval +
                                             0.5870 * gval +
                                             0.1140 * bval))
                    else:
                        self.crop.append(0)     # just add a black pixel
                else:
                    if inside:
                        start = 3 * self.tx * (self.ty - v) + 3 * h
                        self.crop.append(self.img[start])
                        self.crop.append(self.img[start + 1])
                        self.crop.append(self.img[start + 2])
                    else:
                        self.crop.append(0)     # RGB = 0 for a
                        self.crop.append(0)     # black point here
                        self.crop.append(0)

    def select_inside(self):
        self.avg[0] /= 4.0
        self.avg[1] /= 4.0

        # Calculate the determinant of two points based
        # on the center of the quad
        def det(i, j):
            a = self.points[i][0] - self.avg[0]
            b = self.points[i][1] - self.avg[1]
            c = self.points[j][0] - self.avg[0]
            d = self.points[j][1] - self.avg[1]
            return a * d - b * c


        # keep looping until all points are anticlockwise
        # which means all the determinants are negative
        self.det = [0, 0, 0, 0]
        swapped = True
        while swapped:
            swapped = False
            for i in range(0, 4):
                np = (i + 1) % 4
                self.det[i] = det(i, np)
                if self.det[i] > 0.0:
                    swapped = True
                    x = self.points[i]
                    self.points[i] = self.points[np]
                    self.points[np] = x
                    self.det[i] = det(i, np)

        # Calculate the slope and the intercept of each
        # pair of lines
        self.slope = [0, 0, 0, 0]
        self.intercept = [0, 0, 0, 0]
        def slope_intercept(i, j):
            a = self.points[i][0]
            b = self.points[i][1]
            c = self.points[j][0]
            d = self.points[j][1]
            if c - a == 0.0:
                slope = None
                intercept = None
            else:
                slope = (d - b) / (c - a)
                intercept = b - slope * a
            return (slope, intercept)

        for i in range(0, 4):
            np = (i + 1) % 4
            (self.slope[i], self.intercept[i]) = slope_intercept(i, np)


        # Find the min and max for the image
        self.min_x = int(min(self.points[0][0], self.points[1][0],
                         self.points[2][0], self.points[3][0]))
        self.max_x = int(max(self.points[0][0], self.points[1][0],
                         self.points[2][0], self.points[3][0]))
        self.min_y = int(min(self.points[0][1], self.points[1][1],
                         self.points[2][1], self.points[3][1]))
        self.max_y = int(max(self.points[0][1], self.points[1][1],
                         self.points[2][1], self.points[3][1]))

        self.crop = bytearray()

        if True:
            self.crop_image()
        else:
            for v in range(self.min_y, self.max_y + 1):
                for h in range(self.min_x, self.max_x + 1):
                    start = 3 * self.tx * (self.ty - v) + 3 * h
                    self.crop.append(self.img[start])
                    self.crop.append(self.img[start + 1])
                    self.crop.append(self.img[start + 2])

        sx = self.max_x - self.min_x + 1
        sy = self.max_y - self.min_y + 1

        gl_type = GL_RGB
        if self.do_greyscale:
            gl_type = GL_LUMINANCE

        # Now we've got an image in (R,G,B) values. Convert to a texture.
        self.cropped = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.cropped)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, gl_type, sx, sy,
                0, gl_type, GL_UNSIGNED_BYTE, self.crop)

        # flag the display() function to show the cropped image
        self.show_crop = True

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
        self.tx = i.size[0]
        self.ty = i.size[1]
        self.img_ratio = float(self.ty) / float(self.tx)
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
