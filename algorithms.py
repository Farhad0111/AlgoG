# algorithms.py
import pygame
from collections import deque
from queue import PriorityQueue


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def h(p1, p2):
    """Manhattan distance heuristic."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def reconstruct_path(came_from, end, draw):
    """
    Fix #3: Walk came_from from end back to start, INCLUDE the start node,
    return the path ordered start→end, and color only intermediate nodes
    (start/end are re-colored by the caller).

    Returns a list of nodes [start, ..., end].
    """
    path = []
    current = end
    while current in came_from:
        path.append(current)
        current = came_from[current]
        # Color the node we just moved to (predecessor) only if it isn't start
        if current in came_from:
            current.make_path()
        draw()
    path.append(current)   # append start
    path.reverse()         # now ordered start → end
    return path


# ---------------------------------------------------------------------------
# A*
# ---------------------------------------------------------------------------

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]

        # Lazy deletion: skip stale entries (node was re-queued with better score)
        if current not in open_set_hash:
            continue
        open_set_hash.discard(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                # Fix #12 pattern: always re-insert so the queue has the latest score
                count += 1
                open_set.put((f_score[neighbor], count, neighbor))
                open_set_hash.add(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return None


# ---------------------------------------------------------------------------
# Dijkstra  — Fix #12: use lazy-deletion so improved scores are always queued
# ---------------------------------------------------------------------------

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_g, _, current = open_set.get()

        # Lazy deletion: skip stale entries (node was re-queued with better score)
        if current not in open_set_hash:
            continue
        open_set_hash.discard(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                count += 1
                open_set.put((temp_g, count, neighbor))   # re-insert with new score
                open_set_hash.add(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return None


# ---------------------------------------------------------------------------
# BFS
# ---------------------------------------------------------------------------

def bfs(draw, grid, start, end):
    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()
        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return None


# ---------------------------------------------------------------------------
# DFS
# ---------------------------------------------------------------------------

def dfs(draw, grid, start, end):
    stack = [start]
    visited = {start}
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()
        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return None


# ---------------------------------------------------------------------------
# Greedy Best-First
# ---------------------------------------------------------------------------

def greedy_best_first(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((h(start.get_pos(), end.get_pos()), count, start))
    came_from = {}
    visited = {start}
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.discard(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                count += 1
                open_set.put((h(neighbor.get_pos(), end.get_pos()), count, neighbor))
                open_set_hash.add(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return None


# ---------------------------------------------------------------------------
# Bidirectional BFS  — Fix #7: clean path reconstruction, no duplicate meet_node
# ---------------------------------------------------------------------------

def _reconstruct_bidir_path(came_from_start, came_from_end, meet_node, start, end, draw):
    """
    Build a contiguous path [start, ..., meet_node, ..., end].
    meet_node appears exactly once (at the junction).
    """
    # Walk backward from meet_node to start
    forward = []
    node = meet_node
    while node in came_from_start:
        forward.append(node)
        node = came_from_start[node]
    forward.append(start)
    forward.reverse()                   # [start, ..., meet_node]

    # Walk forward from meet_node toward end (via came_from_end)
    # came_from_end maps discovered_node → the end-side BFS parent
    # so following it from meet_node walks toward end
    backward = []
    node = meet_node
    while node in came_from_end:
        node = came_from_end[node]
        backward.append(node)           # excludes meet_node, includes end

    path = forward + backward           # meet_node appears exactly once

    for node in path:
        if node != start and node != end:
            node.make_path()
            draw()

    end.make_end()
    start.make_start()
    return path


def bidirectional_search(draw, grid, start, end):
    queue_start   = deque([start])
    queue_end     = deque([end])
    visited_start = {start}
    visited_end   = {end}
    came_from_start = {}
    came_from_end   = {}
    meet_node = None

    while queue_start and queue_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Expand one step from start side
        current = queue_start.popleft()
        for neighbor in current.neighbors:
            if neighbor not in visited_start:
                visited_start.add(neighbor)
                came_from_start[neighbor] = current
                queue_start.append(neighbor)
                neighbor.make_open()
                if neighbor in visited_end:
                    meet_node = neighbor
                    break
        if meet_node:
            break

        draw()
        if current != start:
            current.make_closed()

        if not queue_end:
            break

        # Expand one step from end side
        current = queue_end.popleft()
        for neighbor in current.neighbors:
            if neighbor not in visited_end:
                visited_end.add(neighbor)
                came_from_end[neighbor] = current
                queue_end.append(neighbor)
                neighbor.make_open()
                if neighbor in visited_start:
                    meet_node = neighbor
                    break
        if meet_node:
            break

        draw()
        if current != end:
            current.make_closed()

    if not meet_node:
        return None

    return _reconstruct_bidir_path(came_from_start, came_from_end, meet_node, start, end, draw)


# ---------------------------------------------------------------------------
# Jump Point Search (4-directional)
# Fix #6: Proper cardinal-only JPS with correct forced-neighbor detection.
# In a 4-connected grid a forced neighbour for horizontal travel exists when
# a perpendicular cell is blocked at the PREVIOUS column but open at the
# current column (you couldn't have reached it cheaply without turning here).
# ---------------------------------------------------------------------------

def jump_point_search(draw, grid, start, end):
    rows      = len(grid)
    cols      = len(grid[0])
    start_pos = start.get_pos()
    end_pos   = end.get_pos()

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def passable(r, c):
        return in_bounds(r, c) and not grid[r][c].is_wall()

    def jump(r, c, dr, dc):
        """
        Scan iteratively from (r, c) in direction (dr,dc).
        Returns the position of a jump point, a corner cell before a wall, or None.
        """
        while True:
            nr, nc = r + dr, c + dc
            if not passable(nr, nc):
                return (r, c)  # Hit a wall, stop before it to allow turning
            if (nr, nc) == end_pos:
                return (nr, nc)

            if dr == 0:  # horizontal movement
                if (not passable(nr - 1, nc - dc) and passable(nr - 1, nc)) or \
                   (not passable(nr + 1, nc - dc) and passable(nr + 1, nc)):
                    return (nr, nc)
            else:        # vertical movement
                if (not passable(nr - dr, nc - 1) and passable(nr, nc - 1)) or \
                   (not passable(nr - dr, nc + 1) and passable(nr, nc + 1)):
                    return (nr, nc)
                    
            # Stop if we cross the target's row/column to allow turning into it
            if dr != 0 and nr == end_pos[0]:
                return (nr, nc)
            if dc != 0 and nc == end_pos[1]:
                return (nr, nc)

            r, c = nr, nc  # Continue iterative scan

    def get_successors(node, parent_pos):
        r, c = node.get_pos()
        successors = []

        if parent_pos is None:
            # Start node: explore all 4 directions
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        else:
            pr, pc = parent_pos
            dr = 0 if r == pr else (1 if r > pr else -1)
            dc = 0 if c == pc else (1 if c > pc else -1)

            # Continue in natural direction and unconditionally probe perpendiculars
            if dr != 0:
                dirs = [(dr, 0), (0, 1), (0, -1)]
            else:
                dirs = [(0, dc), (1, 0), (-1, 0)]

        for ddr, ddc in dirs:
            if passable(r + ddr, c + ddc):
                jp = jump(r, c, ddr, ddc)
                if jp and jp != (r, c):
                    successors.append(jp)

        return successors

    # A* outer loop driving JPS successor generation
    count = 0
    open_set = PriorityQueue()
    open_set.put((h(start_pos, end_pos), count, start, None))
    open_set_hash = {start}
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        _, _, current, parent_pos = open_set.get()

        # Lazy deletion
        if current not in open_set_hash:
            continue
        open_set_hash.discard(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        current_pos = current.get_pos()
        for successor_pos in get_successors(current, parent_pos):
            sr, sc = successor_pos
            successor_node = grid[sr][sc]
            distance  = abs(sr - current_pos[0]) + abs(sc - current_pos[1])
            tentative_g = g_score[current] + distance

            if tentative_g < g_score[successor_node]:
                came_from[successor_node] = current
                g_score[successor_node]   = tentative_g
                f = tentative_g + h(successor_pos, end_pos)
                count += 1
                open_set.put((f, count, successor_node, current_pos))
                open_set_hash.add(successor_node)
                successor_node.make_open()

        draw()
        if current != start:
            current.make_closed()

    return None
