import ctypes
import sys
import pygame
from consts import GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
from mouse_buttons import Mouse
from game_field import GameField
from OpenGL.GL import *  # type: ignore
from OpenGL.GLU import *  # type: ignore

# Set process DPI awareness. Use 1 for "System DPI Awareness", or 2 for "Per-Monitor DPI Awareness"
ctypes.windll.shcore.SetProcessDpiAwareness(1)

pygame.init()

screen = pygame.display.set_mode((1920, 1080), pygame.OPENGL | pygame.DOUBLEBUF)
screen_size = screen.get_size()
glViewport(0, 0, *screen_size)

# Reset projection matrix
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, *screen_size, 0, -1, 1)

mouse = Mouse()

game_field = GameField(GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT)

clock = pygame.time.Clock()

# Set background's color
glClearColor(100 / 255, 100 / 255, 100 / 255, 1.0)

while True:
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            print(f"blocks:{mouse.blocks}")
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print(f"blocks:{mouse.blocks}")
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_s:
                print('saved')
                game_field.save_to_file()
            if event.key == pygame.K_l:
                print('loaded')
                game_field.load_from_file()

    mouse.update(game_field)

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Set modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Draw things
    glBegin(GL_QUADS)

    glColor3f(1, 0, 0)

    # glVertex2f(0, 0)
    # glVertex2f(0 + 100, 0)
    # glVertex2f(0 + 100, 0 + 100)
    # glVertex2f(0, 0 + 100)

    game_field.draw()

    glEnd()

    pygame.display.flip()
    clock.tick(60)
