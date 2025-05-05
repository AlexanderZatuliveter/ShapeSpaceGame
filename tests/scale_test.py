import pygame
from pygame.locals import *
from OpenGL.GL import *

# Define your virtual game field size
VIRTUAL_WIDTH = 800
VIRTUAL_HEIGHT = 600


def calculate_scale(window_width, window_height):
    scale_x = window_width / VIRTUAL_WIDTH
    scale_y = window_height / VIRTUAL_HEIGHT
    return min(scale_x, scale_y)  # Preserve aspect ratio


def draw_square():
    glColor3f(1, 0, 0)  # Red color
    glBegin(GL_QUADS)
    glVertex2f(100, 100)
    glVertex2f(200, 100)
    glVertex2f(200, 200)
    glVertex2f(100, 200)
    glEnd()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768), DOUBLEBUF | OPENGL | RESIZABLE)
    pygame.display.set_caption("OpenGL Scaled 2D Game Field")

    glClearColor(0.2, 0.2, 0.2, 1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, DOUBLEBUF | OPENGL | RESIZABLE)
                glViewport(0, 0, *event.size)

        # Get current window size
        window_width, window_height = pygame.display.get_surface().get_size()

        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Set up projection (no depth, 2D)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT, 0, -1, 1)

        # Set modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Apply scaling
        scale = calculate_scale(window_width, window_height)
        glTranslatef((window_width / scale - VIRTUAL_WIDTH) / 2,
                     (window_height / scale - VIRTUAL_HEIGHT) / 2, 0)
        glScalef(scale, scale, 1)

        # Draw things
        draw_square()

        pygame.display.flip()
        pygame.time.wait(16)

    pygame.quit()


if __name__ == "__main__":
    main()
