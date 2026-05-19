# grid.py
import pygame
from enum import Enum, auto
from constants import *


# ---------------------------------------------------------------------------
# Fix #5: Node state stored as an enum, NOT as a color.
# Changing a render color in _STATE_COLORS never breaks any logic.
# ---------------------------------------------------------------------------
class NodeState(Enum):
    EMPTY       = auto()
    WALL        = auto()
    START       = auto()
    END         = auto()
    OPEN        = auto()
    CLOSED      = auto()
    PATH        = auto()
    PLAYER_PATH = auto()
    OVERLAP     = auto()   # player path overlaps with optimal path

# Single place that maps state → render color
_STATE_COLORS = {
    NodeState.EMPTY:       WHITE,
    NodeState.WALL:        BLACK,
    NodeState.START:       ORANGE,
    NodeState.END:         TURQUOISE,
    NodeState.OPEN:        GREEN,
    NodeState.CLOSED:      RED,
    NodeState.PATH:        BLUE,
    NodeState.PLAYER_PATH: PURPLE,
    NodeState.OVERLAP:     YELLOW,
}


class Node:
    # Fix #4 / #15: parameter renamed to grid_size (used for BOTH row & col bounds)
    def __init__(self, row, col, width, grid_size):
        self.row       = row
        self.col       = col
        self.x         = col * width
        self.y         = row * width
        self.state     = NodeState.EMPTY   # Fix #5: state not color
        self.width     = width
        self.grid_size = grid_size         # Fix #4: single size for square grid
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    # -- State queries (never touch color) --
    def is_closed(self):      return self.state == NodeState.CLOSED
    def is_open(self):        return self.state == NodeState.OPEN
    def is_wall(self):        return self.state == NodeState.WALL
    def is_start(self):       return self.state == NodeState.START
    def is_end(self):         return self.state == NodeState.END
    def is_player_path(self): return self.state == NodeState.PLAYER_PATH

    # -- State mutations --
    def reset(self):           self.state = NodeState.EMPTY
    def make_start(self):      self.state = NodeState.START
    def make_closed(self):     self.state = NodeState.CLOSED
    def make_open(self):       self.state = NodeState.OPEN
    def make_wall(self):       self.state = NodeState.WALL
    def make_end(self):        self.state = NodeState.END
    def make_path(self):        self.state = NodeState.PATH
    def make_player_path(self):  self.state = NodeState.PLAYER_PATH
    def make_overlap(self):      self.state = NodeState.OVERLAP

    def draw(self, win):
        color = _STATE_COLORS[self.state]
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        size = self.grid_size   # Fix #4: use grid_size for BOTH row & col checks
        # DOWN
        if self.row < size - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT
        if self.col < size - 1 and not grid[self.row][self.col + 1].is_wall():  # Fix #4
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):          # Fix #15: still 'rows' because grid is square
            node = Node(i, j, gap, rows)   # Fix #4: pass rows as grid_size
            grid[i].append(node)
    return grid


def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw_grid(win, grid, rows, width):
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid_lines(win, rows, width)
    pygame.draw.line(win, BLACK, (width, 0), (width, HEIGHT), 2)
