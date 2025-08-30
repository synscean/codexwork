"""Minimal Pygame application to verify that the environment works."""

import os
import pygame

# Default window size used when no environment variables are provided.
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480


def get_window_size() -> tuple[int, int]:
    """Determine the window dimensions with optional environment overrides."""
    width_env = os.getenv("PYGAME_WINDOW_WIDTH")
    height_env = os.getenv("PYGAME_WINDOW_HEIGHT")

    try:
        width = int(width_env) if width_env is not None else DEFAULT_WIDTH
    except ValueError:
        width = DEFAULT_WIDTH

    try:
        height = int(height_env) if height_env is not None else DEFAULT_HEIGHT
    except ValueError:
        height = DEFAULT_HEIGHT

    if width <= 0:
        width = DEFAULT_WIDTH
    if height <= 0:
        height = DEFAULT_HEIGHT

    return width, height


def main() -> None:
    """Initialize Pygame and display an empty window until it is closed."""
    # Initialize Pygame modules.
    pygame.init()

    width, height = get_window_size()
    # Create a window using the determined size.
    display_surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pygame Setup Test")

    is_running = True
    while is_running:
        for event in pygame.event.get():
            # Exit when the window is closed or the Escape key is pressed.
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_running = False

        # Fill the window with black to clear previous frames.
        display_surface.fill((0, 0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
