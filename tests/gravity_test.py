import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Параметры объекта
x, y = 100, 100
width, height = 50, 50
velocity_y = 0
gravity = 0.5
jump_strength = -15  # если хочешь добавить прыжок
ground_y = 550

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление прыжком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and y >= ground_y:
        velocity_y = jump_strength

    # Гравитация
    velocity_y += gravity
    y += velocity_y

    # Проверка земли
    if y >= ground_y:
        y = ground_y
        velocity_y = 0

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 200, 0), (x, y, width, height))
    pygame.display.flip()
    clock.tick(60)
