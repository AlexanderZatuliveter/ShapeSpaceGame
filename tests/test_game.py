from typing import Tuple
import pygame
from pygame.locals import *  # type: ignore
from OpenGL.GL import *  # type: ignore
from OpenGL.GLU import *  # type: ignore

# Размер окна
WIDTH, HEIGHT = 800, 600

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL | RESIZABLE)
pygame.display.set_caption("2D OpenGL Game with Pygame")

# Начальная позиция игрока
player_x = 0
player_y = 0
speed = 0.01


def draw_rect(x: int | float, y: int | float, w: int, h: int, color: Tuple[float, float, float]):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


# Настройка 2D проекции
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, WIDTH, 0, HEIGHT)
glMatrixMode(GL_MODELVIEW)

clock = pygame.time.Clock()

running = True
while running:
    glClear(GL_COLOR_BUFFER_BIT)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player_x -= speed * WIDTH
    if keys[K_RIGHT]:
        player_x += speed * WIDTH
    if keys[K_UP]:
        player_y += speed * HEIGHT
    if keys[K_DOWN]:
        player_y -= speed * HEIGHT

    # Отрисовка "игрока"
    draw_rect(player_x, player_y, 50, 50, (0.2, 0.6, 1.0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
