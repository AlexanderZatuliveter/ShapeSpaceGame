from typing import Dict
import pygame
from block import Block
from position import IntPosition
import json


class GameField:
    def __init__(self, width, height):
        self.__block_size = 100
        self.width = width
        self.height = height
        self.field: Dict[tuple[int, int], Block] = {}

    def draw(self):
        for (bx, by), block in self.field.items():
            pos = self._get_block_position(bx, by)
            block.draw((pos.x, pos.y), self.__block_size)

    def _get_block_position(self, bx, by):
        return IntPosition(
            int(bx * self.__block_size),
            int(by * self.__block_size)
        )

    def get_block_field_position(self, x: float, y: float):
        return IntPosition(
            int(x // self.__block_size),
            int(y // self.__block_size)
        )

    def _get_block_rect(self, x: int, y: int):
        return pygame.Rect(x * self.__block_size, y * self.__block_size, self.__block_size, self.__block_size)

    def colliderect_with(self, x, y, rect: pygame.Rect):
        block_pos = self.get_block_field_position(x, y)
        key = (block_pos.x, block_pos.y)
        if key in self.field:
            if rect.colliderect(self._get_block_rect(*key)):
                return True
        return False

    def put_block_by_screen_pos(self, x, y):
        pos = self.get_block_field_position(x, y)
        self.put_block(pos)

    def put_block(self, pos: IntPosition):
        key = (pos.x, pos.y)
        if key not in self.field:
            self.field[key] = Block(pos)

    def hit_block(self, pos: IntPosition):
        key = (pos.x, pos.y)
        if key in self.field:
            del self.field[key]

    def hit_block_by_screen_pos(self, x, y):
        pos = self.get_block_field_position(x, y)
        self.hit_block(pos)

    def save_to_file(self):
        data = {
            "positions": [f"{x}x{y}" for (x, y) in self.field.keys()]
        }
        with open("first.level", "w") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self):
        with open("first.level", "r") as f:
            data = json.load(f)
        self.field.clear()
        for pos_str in data.get("positions", []):
            x, y = map(int, pos_str.split("x"))
            self.put_block(IntPosition(x, y))
