"""Tests for the Pygame application defined in src/main.py."""

import os
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

# Use the "dummy" video driver so that Pygame does not require a windowing system.
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Ensure the src directory is on the Python path for imports.
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pygame
import main as main_module


class TestMain(TestCase):
    """Unit tests for the main module."""

    def test_main_initializes_and_quits(self) -> None:
        """Verify initialization, display setup, event handling, and shutdown."""
        quit_event = pygame.event.Event(pygame.QUIT)
        
        with (
            patch("pygame.init") as mock_init,
            patch("pygame.display.set_mode", return_value=MagicMock()) as mock_set_mode,
            patch("pygame.display.set_caption") as mock_set_caption,
            patch("pygame.event.get", return_value=[quit_event]) as mock_get_events,
            patch("pygame.display.flip") as mock_flip,
            patch("pygame.quit") as mock_quit,
        ):

            # Execute the main loop once. The patched QUIT event terminates the loop immediately.
            main_module.main()

        # Initialization and shutdown should each occur exactly once.
        mock_init.assert_called_once()
        mock_quit.assert_called_once()

        # The display should be created with positive integer dimensions.
        mock_set_mode.assert_called_once()
        (dimensions,), _ = mock_set_mode.call_args
        width, height = dimensions
        self.assertIsInstance(width, int)
        self.assertIsInstance(height, int)
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)

        # The window title should be a meaningful non-empty string.
        mock_set_caption.assert_called_once()
        caption_argument = mock_set_caption.call_args[0][0]
        self.assertIsInstance(caption_argument, str)
        self.assertNotEqual(caption_argument, "")

        # The event loop and frame update should both be performed once.
        mock_get_events.assert_called_once()
        mock_flip.assert_called_once()
