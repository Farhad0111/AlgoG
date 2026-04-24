# ui.py
import pygame
from constants import *

class Button:
    def __init__(self, x, y, width, height, text, color=WHITE, hover_color=LIGHT_BLUE, text_color=BLACK, font_size=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        try:
            self.font = pygame.font.SysFont("comicsans", font_size)
        except:
            self.font = pygame.font.Font(None, font_size)
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_hovered = False
        
    def draw(self, win):
        current_color = self.hover_color if self.is_hovered else self.color
        
        pygame.draw.rect(win, current_color, self.rect)
        pygame.draw.rect(win, BLACK, self.rect, 2) # border
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.is_hovered = True
            else:
                self.is_hovered = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                return True
        return False

def draw_text(win, text, font_size, x, y, color=BLACK, center=False):
    try:
        font = pygame.font.SysFont("comicsans", font_size)
    except:
        font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
        win.blit(text_surface, rect)
    else:
        win.blit(text_surface, (x, y))
