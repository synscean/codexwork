"""Vertical scrolling meteor avoidance game using Pygame."""

from __future__ import annotations

import random
from enum import Enum, auto
from pathlib import Path

import pygame

# Screen dimensions as requested by the user.
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

# Number of stars used to create the scrolling starfield background.
STAR_COUNT = 100

# Custom event for scoring when a meteor passes the bottom of the screen.
METEOR_PASSED_EVENT = pygame.USEREVENT + 1


class GameState(Enum):
    """Represents the different states of the game."""
    PLAYING = auto()
    GAME_OVER = auto()


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
    """A falling meteor that the player must avoid.

    This is the base class for all types of meteors.
    """

    def __init__(self, image: pygame.Surface, x_position: int, speed: int) -> None:
        super().__init__()
        self.image = image
        # Start above the screen, using the image height for the offset.
        self.rect = self.image.get_rect(midtop=(x_position, -image.get_height()))
        self.speed_y = speed
        self.speed_x = 0

    def update(self, *args, **kwargs) -> None:
        """Move the meteor and remove it when off-screen.

        Accepts *args and **kwargs to be compatible with other sprite update
        methods in the same group that might receive arguments.
        """
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > SCREEN_HEIGHT:
            # Post an event to signal a point scored.
            pygame.event.post(pygame.event.Event(METEOR_PASSED_EVENT))
            self.kill()


class StraightMeteor(Meteor):
    """A meteor that falls straight down. The original behavior."""

    # No special behavior, so no methods need to be overridden.
    pass


class ZigzagMeteor(Meteor):
    """A meteor that moves in a zigzag pattern."""

    def __init__(self, image: pygame.Surface, x_position: int, speed: int) -> None:
        super().__init__(image, x_position, speed)
        self.speed_x = random.choice([-3, 3])

    def update(self, *args, **kwargs) -> None:
        """Reverse horizontal direction when hitting screen edges."""
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        super().update(*args, **kwargs)


class HomingMeteor(Meteor):
    """A meteor that slowly homes in on the player's spaceship."""

    def __init__(self, image: pygame.Surface, x_position: int, speed: int) -> None:
        super().__init__(image, x_position, speed)
        # Homing meteors are slightly slower vertically to be less unfair.
        self.speed_y = max(1, speed - 2)
        self.homing_strength = 0.02

    def update(self, *args, **kwargs) -> None:
        """Adjust horizontal speed to move towards the player."""
        player: Spaceship | None = kwargs.get("player")
        if player:
            # Gently adjust horizontal speed towards the player
            direction_x = player.rect.centerx - self.rect.centerx
            self.speed_x += direction_x * self.homing_strength
            # Clamp horizontal speed to a maximum value
            self.speed_x = max(-3, min(3, self.speed_x))
        super().update(*args, **kwargs)


class Shield(pygame.sprite.Sprite):
    """A shield that protects the spaceship from one impact."""

    def __init__(self, spaceship: Spaceship) -> None:
        super().__init__()
        self.spaceship = spaceship
        # Create a surface for the shield, slightly larger than the ship
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Draw a semi-transparent blue arc for the shield effect
        shield_rect = self.image.get_rect()
        pygame.draw.arc(
            self.image,
            (100, 200, 255, 180),  # Light blue, semi-transparent
            shield_rect.inflate(-8, -8),  # Make it a bit smaller than the surface
            0.4,  # Start angle in radians
            2.74,  # Stop angle in radians
            4,  # Width of the arc
        )
        self.rect = self.image.get_rect(center=self.spaceship.rect.center)

    def update(self, *args, **kwargs) -> None:
        """Keep the shield's position centered on the spaceship."""
        self.rect.center = self.spaceship.rect.center


def draw_centered_text(surface: pygame.Surface, text: str, font: pygame.font.Font, color: tuple[int, int, int], y_offset: int = 0) -> None:
    """Render and draw text centered on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset)
    )
    surface.blit(text_surface, text_rect)


def main() -> None:
    """Run the meteor avoidance game."""
    pygame.init()

    display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Meteor Avoidance")

    # Initialize score and font for displaying it.
    score = 0
    # Use the default Pygame font, size 36.
    score_font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 48)

    assets_directory = Path(__file__).resolve().parent / "assets"
    spaceship_image = load_image(assets_directory / "myship.png", 32, 32)
    rock_image = load_image(assets_directory / "rock.png", 32, 32)
    explosion_image = load_image(assets_directory / "explosion.png", 48, 48)

    # A list of available meteor classes and their corresponding images.
    meteor_types = [(StraightMeteor, rock_image), (ZigzagMeteor, rock_image), (HomingMeteor, rock_image)]

    stars = [Star() for _ in range(STAR_COUNT)]
    spaceship = Spaceship(spaceship_image)
    meteor_group = pygame.sprite.Group()
    shield_group = pygame.sprite.GroupSingle()
    all_sprites = pygame.sprite.Group(spaceship)

    clock = pygame.time.Clock()
    game_state = GameState.PLAYING
    is_running = True
    meteor_spawn_interval_ms = 1000
    last_spawn_time = pygame.time.get_ticks()

    while is_running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_running = False

            if game_state == GameState.PLAYING:
                if event.type == METEOR_PASSED_EVENT:
                    score += 1
                    if score > 0 and score % 5 == 0 and not shield_group.sprite:
                        shield = Shield(spaceship)
                        shield_group.add(shield)
                        all_sprites.add(shield)
            elif game_state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        # Reset game to play again
                        score = 0
                        spaceship.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
                        meteor_group.empty()
                        shield_group.empty()
                        all_sprites.empty()
                        all_sprites.add(spaceship)
                        last_spawn_time = pygame.time.get_ticks()
                        game_state = GameState.PLAYING
                    elif event.key == pygame.K_n:
                        is_running = False

        if game_state == GameState.PLAYING:
            # --- Game Logic and Updates ---
            pressed_state = pygame.key.get_pressed()
            move_left = pressed_state[pygame.K_LEFT]
            move_right = pressed_state[pygame.K_RIGHT]

            current_time = pygame.time.get_ticks()
            if current_time - last_spawn_time >= meteor_spawn_interval_ms:
                MeteorClass, meteor_image = random.choice(meteor_types)
                meteor_x = random.randint(0, SCREEN_WIDTH - meteor_image.get_width())
                meteor_speed = random.randint(3, 6)
                meteor = MeteorClass(meteor_image, meteor_x, meteor_speed)
                meteor_group.add(meteor)
                all_sprites.add(meteor)
                last_spawn_time = current_time

            spaceship.update(move_left, move_right)
            meteor_group.update(player=spaceship)
            shield_group.update()
            for star in stars:
                star.update()

            # --- Drawing ---
            display_surface.fill((0, 0, 0))
            for star in stars:
                star.draw(display_surface)
            all_sprites.draw(display_surface)

            score_surface = score_font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
            display_surface.blit(score_surface, score_rect)

            # --- Collision Detection ---
            # Check if the shield is hit, destroying both shield and meteor
            if pygame.sprite.groupcollide(shield_group, meteor_group, True, True):
                # Shield was hit and destroyed, no further action needed
                pass
            # If no shield was hit (or no shield exists), check for player collision
            elif pygame.sprite.spritecollide(spaceship, meteor_group, False):
                explosion_rect = explosion_image.get_rect(center=spaceship.rect.center)
                display_surface.blit(explosion_image, explosion_rect)
                game_state = GameState.GAME_OVER

        elif game_state == GameState.GAME_OVER:
            # --- Draw Game Over Screen ---
            draw_centered_text(display_surface, "GAME OVER", game_over_font, (255, 0, 0), -40)
            draw_centered_text(display_surface, "Continue? (Y/N)", score_font, (255, 255, 255), 20)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
