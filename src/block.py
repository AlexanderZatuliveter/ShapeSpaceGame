

# from typing import Tuple
# import pygame

# from OpenGL.GL import *  # type: ignore

# from position import IntPosition  # type: ignore


# class Block:
#     def __init__(self, pos: IntPosition) -> None:
#         self.__rect = pygame.Rect(pos.x, pos.y, 100, 100)

#     def update(self) -> None:
#         pass

#     def draw(self, pos: IntPosition) -> None:
#         x, y = pos.x, pos.y  # Это уже пиксели, типа (300, 200)
#         size = 100
#         glColor3f(50 / 255, 50 / 255, 50 / 255)
#         glVertex2f(x, y)
#         glVertex2f(x + size, y)
#         glVertex2f(x + size, y + size)
#         glVertex2f(x, y + size)

from typing import Tuple
from OpenGL.GL import *  # type: ignore

from position import IntPosition


class Block:
    def __init__(self, pos: IntPosition) -> None:
        # pos хранится просто для информации, не обязателен
        self.pos = pos

    def update(self) -> None:
        pass

    def draw(self, pixel_pos: Tuple[int, int], size: int) -> None:
        x, y = pixel_pos

        glColor3f(50 / 255, 50 / 255, 50 / 255)
        glVertex2f(x, y)
        glVertex2f(x + size, y)
        glVertex2f(x + size, y + size)
        glVertex2f(x, y + size)
