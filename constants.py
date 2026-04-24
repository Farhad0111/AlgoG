# constants.py
import pygame

# Colors (R, G, B)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0) # Wait, green and blue mix up? Let's fix that.
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
DARK_GREY = (50, 50, 50)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 100, 0)

# Window Dimensions
WIDTH = 1000
HEIGHT = 700
SIDEBAR_WIDTH = 300
GRID_WIDTH = 700

# Grid Settings
ROWS = 25 # default rows

# FPS
FPS = 60

# Game States
STATE_MENU = 0
STATE_DRAWING = 1
STATE_RUNNING_ALGO = 2
STATE_RESULTS = 3
