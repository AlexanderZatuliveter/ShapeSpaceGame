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

target_width = info.current_w * 0.7
target_height = target_width / GAME_FIELD_PROPORTIONS
screen_size = (int(target_width), int(target_height))

screen = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL | RESIZABLE)
pygame.display.set_caption("ShapeSpaceGame")

past_screen_size = screen.get_size()


def resize_display(screen_width: int, screen_height: int) -> None:
    """Handle window resizing while maintaining the aspect ratio."""

    global past_screen_size

    ratio_w = screen_width / GAME_FIELD_WIDTH
    ratio_h = screen_height / GAME_FIELD_HEIGHT

    if past_screen_size > (screen_width, screen_height):
        ratio = min(ratio_w, ratio_h)
    else:
        ratio = max(ratio_w, ratio_h)

    past_screen_size = pygame.display.get_window_size()

    new_width = int(GAME_FIELD_WIDTH * ratio)
    new_height = int(GAME_FIELD_HEIGHT * ratio)

    # Set up the viewport to maintain aspect ratio
    screen = pygame.display.set_mode((new_width, new_height), DOUBLEBUF | OPENGL | RESIZABLE)
    glViewport(0, 0, new_width, new_height)

    # Reset projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT, 0, -1, 1)


# Initialize window
resize_display(*screen_size)
clock = pygame.time.Clock()
player = Player()

glClearColor(100 / 255, 100 / 255, 100 / 255, 1)  # Set background's color

# turn on smooth lines and blending
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

while True:

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
            resize_display(event.w, event.h)

    player.update(keys)

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Set modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Draw game field border (10 pixels from each edge)
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    glVertex2f(10, 10)
    glVertex2f(GAME_FIELD_WIDTH - 10, 10)
    glVertex2f(GAME_FIELD_WIDTH - 10, GAME_FIELD_HEIGHT - 10)
    glVertex2f(10, GAME_FIELD_HEIGHT - 10)
    glEnd()

    # Draw things
    glBegin(GL_QUADS)
    player.draw()
    glEnd()

    pygame.display.flip()

    clock.tick(60)
