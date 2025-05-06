import pygame
from pygame.key import ScancodeWrapper
from OpenGL.GL import *  # type: ignore
import random
from consts import GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH, PLAYER_JUMP_FORCE, PLAYER_SPEED, GRAVITY


class Player:
    def __init__(self) -> None:
        # self.__rect = pygame.Rect(GAME_FIELD_WIDTH // 2, GAME_FIELD_HEIGHT // 2, 100, 100)
        self.__rect = pygame.Rect(
            int(GAME_FIELD_WIDTH * random.random()),
            int(GAME_FIELD_HEIGHT * random.random()),
            100,
            100
        )

        self.__velocity_y = 0
        self.__gravity = GRAVITY
        self.__jump_force = -PLAYER_JUMP_FORCE

    def update(self, keys: ScancodeWrapper) -> None:
        if keys[pygame.K_a] and self.__rect.topleft[0] > 0:
            self.__rect.centerx -= PLAYER_SPEED
        if keys[pygame.K_d] and self.__rect.bottomright[0] < GAME_FIELD_WIDTH:
            self.__rect.centerx += PLAYER_SPEED

        if keys[pygame.K_w] and self.__rect.bottom >= GAME_FIELD_HEIGHT:
            self.__velocity_y = self.__jump_force

        # Gravitation
        self.__velocity_y += self.__gravity
        self.__rect.centery += int(self.__velocity_y)

        if self.__rect.bottom >= GAME_FIELD_HEIGHT:
            self.__rect.bottom = GAME_FIELD_HEIGHT
            self.__velocity_y = 0

    def draw(self) -> None:
        glColor3f(0, 0, 1)
        glVertex2f(self.__rect.x, self.__rect.y)
        glVertex2f(self.__rect.x + self.__rect.w, self.__rect.y)
        glVertex2f(self.__rect.x + self.__rect.w, self.__rect.y + self.__rect.h)
        glVertex2f(self.__rect.x, self.__rect.y + self.__rect.h)
