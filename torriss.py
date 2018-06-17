import pygame
from pygame.locals import *
from itertools import product
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
import random
from math import *


# HEY YOU
# READING THAT SOURCE CODE
# RECOGNIZE THAT THIS IS A SUPER ROUGH THING
# ADDITIONALLY, FORGIVE ME FOR EVERYTHING WRONG
# SERIOUSLY
# I'M SORRY
# PLEASE.
# -JUNE

lastPosX = 0
lastPosY = 0
zoomScale = 1.0
dataL = 0
xRot = 0
yRot = 0
zRot = 0

# Torus Variables
# Cross section segments
m = 10
# Donut segments
n = 100


def Torus(m, n, size, ring_size=None):
    points = [np.array([0, 0, size], dtype=np.float)]
    rotation_1 = np.array([[1, 0, 0],
                          [0, cos(2*pi / m), sin(2*pi/m)],
                          [0, -sin(2*pi / m), cos(2*pi/m)]]),
    rotation_2 = np.array([[cos(2*pi / n), sin(2*pi / n), 0],
                           [-sin(2*pi / n), cos(2*pi / n), 0],
                           [0, 0, 1]]),
    for k in range(1, m):
        points.append(np.matmul(points[-1], rotation_1))
    if ring_size is not None:
        size = ring_size
    shift_vector = np.array([0, -2*size,0], dtype=np.float)
    for k in points:
        k += shift_vector
    torus = [points]
    for k in range(1, n):
        torus.append(list(torus[-1]))
        torus[-1] = [np.matmul(i, rotation_2) for i in torus[-1]]
    glBegin(GL_LINES)
    for h, i in enumerate(torus):
        for j, k in enumerate(i):
            glVertex3fv(k)
            glVertex3fv(i[(j+1) % len(i)])
            glVertex3fv(k)
            glVertex3fv(torus[(h+1) % len(torus)][j])
    glEnd()


def mouseMove(event):
    # ADDITIONALLY, RECOGNIZE THAT I COPIED/PASTED THIS FROM SOME JABRONI
    # THE JABRONI IS LOCATED HERE
    # http://goldsequence.blogspot.com/2017/04/using-mouse-for-object-zoom-inzoom.html


    # THIS LINE IS THE PRIMARY REASON I'M DISAVOWING THIS CODE, USING GLOBALS IS WRONG
    # BUT I DON'T WANNA TAKE THE TIME TO FIGURE OUT HOW TO DO IT RIGHT, SO UNTIL I
    # REWRITE THIS ENTIRE ATROCITY, RE: NEVER, I WILL NOT FIX IT.
    global lastPosX, lastPosY, zoomScale, xRot, yRot, zRot;

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4: # wheel rolled up
        glScaled(1.05, 1.05, 1.05)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: # wheel rolled down
        glScaled(0.95, 0.95, 0.95)

    if event.type == pygame.MOUSEMOTION:
        x, y = event.pos
        dx = x - lastPosX
        dy = y - lastPosY

        mouseState = pygame.mouse.get_pressed()
        if mouseState[0]:

            modelView = (GLfloat * 16)()
            mvm = glGetFloatv(GL_MODELVIEW_MATRIX, modelView)

   # To combine x-axis and y-axis rotation
            temp = (GLfloat * 3)()
            temp[0] = modelView[0]*dy + modelView[1]*dx
            temp[1] = modelView[4]*dy + modelView[5]*dx
            temp[2] = modelView[8]*dy + modelView[9]*dx
            norm_xy = sqrt(temp[0]*temp[0] + temp[1]*temp[1] + temp[2]*temp[2])
            glRotatef(sqrt(dx*dx+dy*dy), temp[0]/norm_xy, temp[1]/norm_xy, temp[2]/norm_xy)

        lastPosX = x
        lastPosY = y


def main():
    pygame.init()
    display = (1800,1000)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL, RESIZABLE)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -10)
    glRotatef(90,0,1,1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            mouseMove(event)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Torus(m, n, 2)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
