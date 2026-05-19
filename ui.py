# ui.py
"""
UI Module for AlgoG Pathfinding Challenge
Handles button rendering, text drawing, and user interface components.
"""
import pygame
from constants import *


# ============================================================================
# FONT UTILITIES — Fix #14: cache fonts by size to avoid re-creating each frame
# ============================================================================

_font_cache: dict = {}

def _load_font(size: int) -> pygame.font.Font:
    """Return a cached font for *size*. Falls back to the default font."""
    if size not in _font_cache:
        try:
            _font_cache[size] = pygame.font.SysFont("comicsans", size)
        except Exception:
            _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]


# ============================================================================
# BUTTON CLASS
# ============================================================================

class Button:
    """
    Interactive button UI component with hover effects and click detection.

    Attributes:
        rect        (pygame.Rect): Button position and size
        text        (str):         Button display text
        color       (tuple):       RGB color when not hovered
        hover_color (tuple):       RGB color when hovered
        text_color  (tuple):       RGB text color
        font        (pygame.font.Font): Cached font object
        is_hovered  (bool):        Tracks hover state
    """

    def __init__(self, x, y, width, height, text,
                 color=WHITE, hover_color=LIGHT_BLUE,
                 text_color=BLACK, font_size=24):
        self.rect        = pygame.Rect(x, y, width, height)
        self.text        = text
        self.color       = color
        self.hover_color = hover_color
        self.text_color  = text_color
        self.font        = _load_font(font_size)
        self.is_hovered  = False

    def draw(self, win):
        """Draw the button on *win*."""
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(win, current_color, self.rect)
        pygame.draw.rect(win, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect    = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Handle mouse events.

        Returns:
            bool: True if the button was clicked this event.
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.is_hovered)


# ============================================================================
# TEXT RENDERING UTILITY
# ============================================================================

def draw_text(win, text, font_size, x, y, color=BLACK, center=False):
    """
    Draw *text* on *win*.  Uses cached fonts (Fix #14).

    Args:
        center (bool): If True, (x, y) is the centre; otherwise top-left.
    """
    font         = _load_font(font_size)          # cached — no allocation
    text_surface = font.render(text, True, color)
    rect = (text_surface.get_rect(center=(x, y))
            if center
            else text_surface.get_rect(topleft=(x, y)))
    win.blit(text_surface, rect)

# Fix #10: ButtonGroup was defined but never used anywhere — removed.
