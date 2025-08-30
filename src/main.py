"""Vertical scrolling meteor avoidance game using Pygame."""

from __future__ import annotations

import random
from pathlib import Path

import pygame

# Screen dimensions as requested by the user.
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

# Number of stars used to create the scrolling starfield background.
STAR_COUNT = 100


def load_image(image_path: Path, width: int, height: int) -> pygame.Surface:
    """Load an image from *image_path* or create a placeholder surface.

    The placeholder helps the application run even if the expected image
    files are not available. This allows unit tests to execute in environments
    where external assets cannot be downloaded.
    """
    if image_path.is_file():
        return pygame.image.load(str(image_path)).convert_alpha()

    placeholder_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    placeholder_surface.fill((255, 0, 255))  # Magenta placeholder color.
    return placeholder_surface


class Star:
    """A single star that scrolls downward to simulate movement in space."""

    def __init__(self) -> None:
        self.x_position = random.randint(0, SCREEN_WIDTH - 1)
        self.y_position = random.randint(0, SCREEN_HEIGHT - 1)
        self.speed = random.uniform(1.0, 3.0)
        self.size = random.randint(1, 3)

    def update(self) -> None:
        """Move the star downward and wrap it back to the top when needed."""
        self.y_position += self.speed
        if self.y_position > SCREEN_HEIGHT:
            self.y_position = 0
            self.x_position = random.randint(0, SCREEN_WIDTH - 1)

    def draw(self, surface: pygame.Surface) -> None:
        """Render the star on the provided *surface*."""
        surface.fill(
            (255, 255, 255),
            (int(self.x_position), int(self.y_position), self.size, self.size),
        )


class Spaceship(pygame.sprite.Sprite):
    """Player-controlled spaceship that can move left or right."""

    def __init__(self, image: pygame.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        )
        self.speed = 5

    def update(self, move_left: bool, move_right: bool) -> None:
        """Update the spaceship position based on player input."""
        if move_left:
            self.rect.x -= self.speed
        if move_right:
            self.rect.x += self.speed

        # Keep the spaceship within the horizontal bounds of the screen.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Meteor(pygame.sprite.Sprite):
    """A falling meteor that the player must avoid."""

    def __init__(self, image: pygame.Surface, x_position: int, speed: int) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midtop=(x_position, -32))
        self.speed = speed

    def update(self) -> None:
        """Move the meteor downward and remove it when off-screen."""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


def main() -> None:
    """Run the meteor avoidance game."""
    pygame.init()

    display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Meteor Avoidance")

    assets_directory = Path(__file__).resolve().parent / "assets"
    spaceship_image = load_image(assets_directory / "spaceship.png", 32, 32)
    meteor_image = load_image(assets_directory / "meteor.png", 32, 32)
    explosion_image = load_image(assets_directory / "explosion.png", 48, 48)

    stars = [Star() for _ in range(STAR_COUNT)]
    spaceship = Spaceship(spaceship_image)
    meteor_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(spaceship)

    clock = pygame.time.Clock()
    is_running = True
    meteor_spawn_interval_ms = 1000
    last_spawn_time = pygame.time.get_ticks()

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_running = False

        move_left = False
        move_right = False
        if pygame.get_init():
            pressed_state = pygame.key.get_pressed()
            move_left = pressed_state[pygame.K_LEFT]
            move_right = pressed_state[pygame.K_RIGHT]

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= meteor_spawn_interval_ms:
            meteor_x = random.randint(0, SCREEN_WIDTH - 32)
            meteor_speed = random.randint(3, 6)
            meteor = Meteor(meteor_image, meteor_x, meteor_speed)
            meteor_group.add(meteor)
            all_sprites.add(meteor)
            last_spawn_time = current_time

        spaceship.update(move_left, move_right)
        meteor_group.update()
        for star in stars:
            star.update()

        display_surface.fill((0, 0, 0))
        for star in stars:
            star.draw(display_surface)
        all_sprites.draw(display_surface)

        if pygame.sprite.spritecollide(spaceship, meteor_group, False):
            # Display an explosion and pause briefly before exiting.
            explosion_rect = explosion_image.get_rect(center=spaceship.rect.center)
            display_surface.blit(explosion_image, explosion_rect)
            pygame.display.flip()
            pygame.time.delay(1000)
            break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
