"""Minimal Pygame application to verify the environment works."""

import pygame


def main() -> None:
    """Initialize Pygame and display an empty window until it is closed."""
    pygame.init()

    # Create a window with a fixed size
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pygame Setup Test")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a color to clear old frames
        screen.fill((0, 0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
