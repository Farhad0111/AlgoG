# constants.py
import pygame

# Colors (R, G, B)
RED        = (255, 0,   0)
GREEN      = (0,   255, 0)
BLUE       = (0,   0,   255)   # Fix #9: removed dead double-assignment with debug comment
YELLOW     = (255, 255, 0)
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
PURPLE     = (128, 0,   128)
ORANGE     = (255, 165, 0)
GREY       = (128, 128, 128)
TURQUOISE  = (64,  224, 208)
DARK_GREY  = (50,  50,  50)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN= (144, 238, 144)
DARK_GREEN = (0,   100, 0)

# Window Dimensions
WIDTH        = 1200
HEIGHT       = 800
SIDEBAR_WIDTH= 450
GRID_WIDTH   = 750

# Grid Settings
ROWS = 25  # grid is always square (ROWS × ROWS)

# FPS
FPS = 60

# Game States
STATE_MENU         = 0   # reserved for a future main-menu screen
STATE_DRAWING      = 1
STATE_RUNNING_ALGO = 2
STATE_RESULTS      = 3
