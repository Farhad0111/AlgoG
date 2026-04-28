# ui.py
"""
UI Module for AlgoG Pathfinding Challenge
Handles button rendering, text drawing, and user interface components.
"""
import pygame
from constants import *


# ============================================================================
# FONT UTILITIES
# ============================================================================

def _load_font(size):
    """
    Load a font with fallback support.
    
    Args:
        size (int): Font size in pixels
    
    Returns:
        pygame.font.Font: Loaded font object
    """
    try:
        return pygame.font.SysFont("comicsans", size)
    except Exception:
        return pygame.font.Font(None, size)


# ============================================================================
# BUTTON CLASS
# ============================================================================

class Button:
    """
    Interactive button UI component with hover effects and click detection.
    
    Attributes:
        rect (pygame.Rect): Button position and size
        text (str): Button display text
        color (tuple): RGB color when not hovered
        hover_color (tuple): RGB color when hovered
        text_color (tuple): RGB text color
        font (pygame.font.Font): Rendered font object
        is_hovered (bool): Tracks hover state
    """
    
    def __init__(self, x, y, width, height, text, color=WHITE, hover_color=LIGHT_BLUE, text_color=BLACK, font_size=24):
        """
        Initialize a button at the specified position and size.
        
        Args:
            x (int): X position in pixels
            y (int): Y position in pixels
            width (int): Button width in pixels
            height (int): Button height in pixels
            text (str): Display text
            color (tuple): RGB color (default: WHITE)
            hover_color (tuple): RGB hover color (default: LIGHT_BLUE)
            text_color (tuple): RGB text color (default: BLACK)
            font_size (int): Font size in pixels (default: 24)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = _load_font(font_size)
        self.is_hovered = False

    def draw(self, win):
        """
        Draw the button on the given surface.
        
        Args:
            win (pygame.Surface): Target surface to draw on
        """
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Draw button background
        pygame.draw.rect(win, current_color, self.rect)
        
        # Draw button border
        pygame.draw.rect(win, BLACK, self.rect, 2)
        
        # Draw button text centered
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Handle mouse events for button interaction.
        
        Args:
            event (pygame.event.EventType): Pygame event to process
        
        Returns:
            bool: True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered


# ============================================================================
# TEXT RENDERING UTILITIES
# ============================================================================

def draw_text(win, text, font_size, x, y, color=BLACK, center=False):
    """
    Draw text on the given surface with optional centering.
    
    Args:
        win (pygame.Surface): Target surface to draw on
        text (str): Text content to render
        font_size (int): Font size in pixels
        x (int): X position
        y (int): Y position
        color (tuple): RGB text color (default: BLACK)
        center (bool): If True, position is treated as center; else top-left (default: False)
    """
    font = _load_font(font_size)
    text_surface = font.render(text, True, color)
    
    if center:
        rect = text_surface.get_rect(center=(x, y))
    else:
        rect = text_surface.get_rect(topleft=(x, y))
    
    win.blit(text_surface, rect)


# ============================================================================
# BUTTON MANAGER (For organizing multiple buttons)
# ============================================================================

class ButtonGroup:
    """
    Manages a collection of buttons as a group.
    Useful for organizing related buttons (e.g., algorithm selection, map selection).
    """
    
    def __init__(self, name="ButtonGroup"):
        """
        Initialize a button group.
        
        Args:
            name (str): Identifier for this group
        """
        self.name = name
        self.buttons = {}

    def add_button(self, button_id, button):
        """
        Add a button to the group.
        
        Args:
            button_id (str): Unique identifier for the button
            button (Button): Button instance to add
        """
        self.buttons[button_id] = button

    def draw_all(self, win):
        """Draw all buttons in the group."""
        for button in self.buttons.values():
            button.draw(win)

    def handle_events(self, event):
        """
        Handle events for all buttons in the group.
        
        Args:
            event (pygame.event.EventType): Pygame event
        
        Returns:
            str or None: ID of clicked button, or None if no button was clicked
        """
        for button_id, button in self.buttons.items():
            if button.handle_event(event):
                return button_id
        return None

    def get_button(self, button_id):
        """Get a button by its ID."""
        return self.buttons.get(button_id)

    def get_all(self):
        """Get all buttons in the group."""
        return self.buttons
