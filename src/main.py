import sys
import pygame
import ctypes
from pygame.locals import DOUBLEBUF, OPENGL, RESIZABLE
from OpenGL.GL import *  # type: ignore
from OpenGL.GLU import *

from consts import GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
from player import Player  # type: ignore


# Set process DPI awareness. Use 1 for "System DPI Awareness", or 2 for "Per-Monitor DPI Awareness"
ctypes.windll.shcore.SetProcessDpiAwareness(1)

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=100)

info = pygame.display.Info()

screen_size = info.current_w * 0.7, info.current_h * 0.7

screen = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL | RESIZABLE)
pygame.display.set_caption("ShapeSpaceGame")

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, screen_size[0], screen_size[1], 0)  # (left, right, bottom, top)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

clock = pygame.time.Clock()

player = Player()


while True:
    glClearColor(100 / 255, 100 / 255, 100 / 255, 1)  # set background's color
    glClear(GL_COLOR_BUFFER_BIT)  # clear screen

    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen_size = event.w, event.h
            glViewport(0, 0, event.w, event.h)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluOrtho2D(0, event.w, event.h, 0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

    player.update(keys)

    # OpenGL drawing.

    glBegin(GL_LINE_LOOP)

    width = GAME_FIELD_WIDTH
    height = GAME_FIELD_HEIGHT
    glColor3f(1, 1, 1)
    glVertex2f(0, 0)
    glVertex2f(0 + width, 0)
    glVertex2f(0 + width, 0 + height)
    glVertex2f(0, 0 + height)

    glEnd()

    glBegin(GL_QUADS)
    player.draw()
    glEnd()

    pygame.display.flip()

    clock.tick(60)
