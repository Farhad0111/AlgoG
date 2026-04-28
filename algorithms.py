# algorithms.py
import pygame
from collections import deque
from queue import PriorityQueue

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
        current.make_path()
        draw()
    return path

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
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return None

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

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return None


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
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((h(neighbor.get_pos(), end.get_pos()), count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return None


def reconstruct_bidirectional_path(came_from_start, came_from_end, meet_node, start, end, draw):
    path = []
    node = meet_node

    while node in came_from_start:
        path.append(node)
        node = came_from_start[node]
    path.append(start)
    path.reverse()

    node = meet_node
    while node in came_from_end:
        node = came_from_end[node]
        path.append(node)

    for node in path:
        if node != start and node != end:
            node.make_path()
            draw()

    end.make_end()
    start.make_start()
    return path


def bidirectional_search(draw, grid, start, end):
    queue_start = deque([start])
    queue_end = deque([end])
    visited_start = {start}
    visited_end = {end}
    came_from_start = {}
    came_from_end = {}
    meet_node = None

    while queue_start and queue_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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

    return reconstruct_bidirectional_path(came_from_start, came_from_end, meet_node, start, end, draw)


def jump_point_search(draw, grid, start, end):
    rows = len(grid)
    cols = len(grid[0])
    start_pos = start.get_pos()
    end_pos = end.get_pos()

    def in_bounds(pos):
        r, c = pos
        return 0 <= r < rows and 0 <= c < cols

    def passable(pos):
        return in_bounds(pos) and not grid[pos[0]][pos[1]].is_wall()

    def get_node(pos):
        return grid[pos[0]][pos[1]]

    def jump(pos, direction):
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if not passable(next_pos):
            return None
        if next_pos == end_pos:
            return next_pos

        if direction[0] == 0:
            if passable((next_pos[0] - 1, next_pos[1])) or passable((next_pos[0] + 1, next_pos[1])):
                return next_pos
        else:
            if passable((next_pos[0], next_pos[1] - 1)) or passable((next_pos[0], next_pos[1] + 1)):
                return next_pos

        return jump(next_pos, direction)

    def get_successors(node, parent_pos):
        pos = node.get_pos()
        successors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        if parent_pos is None:
            for direction in directions:
                next_pos = jump(pos, direction)
                if next_pos:
                    successors.append(next_pos)
        else:
            direction = (pos[0] - parent_pos[0], pos[1] - parent_pos[1])
            next_pos = jump(pos, direction)
            if next_pos:
                successors.append(next_pos)

            if direction[0] == 0:
                perpendicular = [(1, 0), (-1, 0)]
            else:
                perpendicular = [(0, 1), (0, -1)]

            for perp in perpendicular:
                if passable((pos[0] + perp[0], pos[1] + perp[1])):
                    next_pos = jump(pos, perp)
                    if next_pos:
                        successors.append(next_pos)

        return successors

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
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return path

        current_pos = current.get_pos()
        successors = get_successors(current, parent_pos)

        for successor_pos in successors:
            successor_node = get_node(successor_pos)
            distance = abs(successor_pos[0] - current_pos[0]) + abs(successor_pos[1] - current_pos[1])
            tentative_g = g_score[current] + distance

            if tentative_g < g_score[successor_node]:
                came_from[successor_node] = current
                g_score[successor_node] = tentative_g
                f_score = tentative_g + h(successor_pos, end_pos)

                if successor_node not in open_set_hash:
                    count += 1
                    open_set.put((f_score, count, successor_node, current_pos))
                    open_set_hash.add(successor_node)
                    successor_node.make_open()

        draw()

        if current != start:
            current.make_closed()

    return None
