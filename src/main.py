import sys
import pygame
import ctypes
from pygame.locals import DOUBLEBUF, OPENGL, RESIZABLE


# Set process DPI awareness. Use 1 for "System DPI Awareness", or 2 for "Per-Monitor DPI Awareness"
ctypes.windll.shcore.SetProcessDpiAwareness(1)

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=100)

info = pygame.display.Info()

screen_size = info.current_w * 0.7, info.current_h * 0.7

screen = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL | RESIZABLE)
pygame.display.set_caption("ShapeSpaceGame")

clock = pygame.time.Clock()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
