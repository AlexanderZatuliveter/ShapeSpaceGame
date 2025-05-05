import pygame
from pygame.key import ScancodeWrapper
from OpenGL.GL import *  # type: ignore

from consts import GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH, PLAYER_SPEED


class Player:
    def __init__(self) -> None:
        self.__rect = pygame.Rect(GAME_FIELD_WIDTH // 2, GAME_FIELD_HEIGHT // 2, 100, 100)

    def update(self, keys: ScancodeWrapper) -> None:
        if keys[pygame.K_LEFT] and self.__rect.topleft[0] > 0:
            self.__rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.__rect.bottomright[0] < GAME_FIELD_WIDTH:
            self.__rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.__rect.topleft[1] > 0:
            self.__rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.__rect.bottomright[1] < GAME_FIELD_HEIGHT:
            self.__rect.y += PLAYER_SPEED

    def draw(self) -> None:
        glColor3f(0, 0, 1)
        glVertex2f(self.__rect.x, self.__rect.y)
        glVertex2f(self.__rect.x + self.__rect.w, self.__rect.y)
        glVertex2f(self.__rect.x + self.__rect.w, self.__rect.y + self.__rect.h)
        glVertex2f(self.__rect.x, self.__rect.y + self.__rect.h)
