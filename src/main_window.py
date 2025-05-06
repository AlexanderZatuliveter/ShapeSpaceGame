
import sys
from typing import Tuple
import pygame
from pygame import Surface
from pygame.time import Clock
from pygame.locals import DOUBLEBUF, OPENGL, RESIZABLE
from OpenGL.GL import *  # type: ignore
from OpenGL.GLU import *  # type: ignore

from consts import GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
from player import Player


class MainWindow:

    def __init__(self, screen: Surface, clock: Clock) -> None:
        self.__screen = screen
        self.__clock = clock
        self.__past_screen_size = self.__screen.get_size()

        self.__player = Player()

    def __resize_display(self, new_screen_size: Tuple[int, int]) -> None:
        """Handle window resizing while maintaining the aspect ratio."""

        if self.__past_screen_size == new_screen_size:
            return

        ratio_w = new_screen_size[0] / GAME_FIELD_WIDTH
        ratio_h = new_screen_size[1] / GAME_FIELD_HEIGHT

        if self.__past_screen_size[0] != new_screen_size[0] and self.__past_screen_size[1] != new_screen_size[1]:
            ratio = min(ratio_w, ratio_h)
        elif self.__past_screen_size[0] != new_screen_size[0]:
            ratio = ratio_w
        elif self.__past_screen_size[1] != new_screen_size[1]:
            ratio = ratio_h

        new_width = int(GAME_FIELD_WIDTH * ratio)
        new_height = int(GAME_FIELD_HEIGHT * ratio)

        self.__set_screen_size((new_width, new_height))

        self.__past_screen_size = pygame.display.get_window_size()

    def __set_screen_size(self, screen_size: Tuple[int, int]) -> None:
        # Set up the viewport to maintain aspect ratio
        self.__screen = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL | RESIZABLE)
        glViewport(0, 0, *screen_size)

        # Reset projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT, 0, -1, 1)

    def show(self) -> None:

        self.__set_screen_size(self.__screen.get_size())

        # Set background's color
        glClearColor(100 / 255, 100 / 255, 100 / 255, 1)

        # turn on smooth lines and blending
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        while True:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            # Updates
            self.update(events)
            self.__player.update(keys)

            # Draws
            self.begin_draw()
            self.__player.draw()
            self.end_draw()

    def update(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.VIDEORESIZE:
                self.__resize_display(event.size)

    def begin_draw(self) -> None:
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

    def end_draw(self) -> None:
        glEnd()
        pygame.display.flip()
        self.__clock.tick(60)
