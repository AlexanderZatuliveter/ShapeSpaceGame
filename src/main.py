import sys
import pygame
import ctypes
from pygame.locals import DOUBLEBUF, OPENGL, RESIZABLE
from OpenGL.GL import *  # type: ignore
from OpenGL.GLU import *  # type: ignore

from consts import GAME_FIELD_HEIGHT, GAME_FIELD_PROPORTIONS, GAME_FIELD_WIDTH
from player import Player


# Set process DPI awareness. Use 1 for "System DPI Awareness", or 2 for "Per-Monitor DPI Awareness"
ctypes.windll.shcore.SetProcessDpiAwareness(1)

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=100)

info = pygame.display.Info()

screen_size = info.current_w * 0.7, info.current_h * 0.7

screen = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL | RESIZABLE)
pygame.display.set_caption("ShapeSpaceGame")

past_screen_size = screen.get_size()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, screen_size[0], screen_size[1], 0)  # (left, right, bottom, top)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

clock = pygame.time.Clock()

player = Player()


scale = GAME_FIELD_WIDTH / screen.get_width()

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
            screen_width, screen_height = event.w, event.h

            new_scale_width = screen_width / GAME_FIELD_WIDTH
            new_scale_height = screen_height / GAME_FIELD_HEIGHT

            new_scale = min(new_scale_width, new_scale_height)
            scale = new_scale

            calculated_width = int(GAME_FIELD_WIDTH * new_scale)
            calculated_height = int(GAME_FIELD_HEIGHT * new_scale)

            screen = pygame.display.set_mode(
                (calculated_width, calculated_height),
                DOUBLEBUF | OPENGL | RESIZABLE
            )

            past_screen_size = screen.get_size()

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluOrtho2D(0, calculated_width, calculated_height, 0)  # (left, right, bottom, top)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()


            # # Настраиваем OpenGL для нового размера
            # glViewport(0, 0, calculated_width, calculated_height)

            # # Настраиваем проекцию
            # glMatrixMode(GL_PROJECTION)
            # glLoadIdentity()

            # # Используем размер игрового поля для ортогональной проекции
            # gluOrtho2D(0, calculated_width, calculated_height, 0)

            # # Возвращаемся в режим модели
            # glMatrixMode(GL_MODELVIEW)
            # glLoadIdentity()

            # # Применяем масштаб
            # glScalef(new_scale, new_scale, 1.0)

    player.update(keys)

    # отрисовка OpenGL

    glBegin(GL_LINE_LOOP)

    width = GAME_FIELD_WIDTH
    height = GAME_FIELD_HEIGHT
    glColor3f(1, 1, 1)
    glVertex2f(10, 10)
    glVertex2f(width * scale - 10, 10)
    glVertex2f(width * scale - 10, height * scale - 10)
    glVertex2f(10, height * scale - 10)

    glEnd()

    glBegin(GL_QUADS)
    player.draw(scale)
    glEnd()

    pygame.display.flip()

    clock.tick(60)
