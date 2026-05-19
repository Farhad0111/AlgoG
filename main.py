# pyrefly: ignore [missing-import]
import pygame
import sys
from constants import *
from grid import make_grid, draw_grid
from algorithms import a_star, dijkstra, bfs, dfs, greedy_best_first, bidirectional_search, jump_point_search
from ui import Button, draw_text
from levels import load_level

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Challenge")


# ---------------------------------------------------------------------------
# Fix #1: get_clicked_pos — correct x/y naming (pygame returns (x, y))
# ---------------------------------------------------------------------------
def get_clicked_pos(pos, rows, width):
    """Return (row, col) for a pixel position, or None if outside the grid."""
    x, y = pos                          # x=horizontal, y=vertical
    if x > width:                       # clicked in the sidebar
        return None
    col = x // (width // rows)          # horizontal px → column
    row = y // (width // rows)          # vertical   px → row
    if 0 <= row < rows and 0 <= col < rows:
        return row, col
    return None


def apply_level(grid, level_name, rows):
    for row in grid:
        for node in row:
            node.reset()

    start_pos, end_pos, walls = load_level(level_name, rows)

    start_node = grid[start_pos[0]][start_pos[1]]
    end_node   = grid[end_pos[0]][end_pos[1]]

    start_node.make_start()
    end_node.make_end()

    for r, c in walls:
        grid[r][c].make_wall()

    return start_node, end_node


# ---------------------------------------------------------------------------
# Fix #16: full redraw helper — sidebar + grid before each display.update()
# ---------------------------------------------------------------------------
def full_draw(win, grid, rows, buttons_to_draw, selected_algo,
              state, player_finished, show_color_info,
              player_steps, algo_steps):
    win.fill(WHITE)
    pygame.draw.rect(win, LIGHT_BLUE, (GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
    draw_grid(win, grid, rows, GRID_WIDTH)

    for btn in buttons_to_draw:
        btn.draw(win)

    if show_color_info:
        _draw_color_legend(win)
    else:
        _draw_stats(win, state, player_steps, algo_steps)


def _draw_color_legend(win):
    panel_x, panel_y = GRID_WIDTH + 15, 470
    panel_w, panel_h = 415, 210
    pygame.draw.rect(win, WHITE, (panel_x, panel_y, panel_w, panel_h))
    pygame.draw.rect(win, BLACK, (panel_x, panel_y, panel_w, panel_h), 2)
    draw_text(win, "Color Legend", 26, panel_x + panel_w // 2, panel_y + 20, color=BLACK, center=True)

    legend_items = [
        ("Start",          ORANGE),
        ("End",            TURQUOISE),
        ("Wall",           BLACK),
        ("Open Nodes",     GREEN),
        ("Closed Nodes",   RED),
        ("Algorithm Path", BLUE),
        ("Your Path",      PURPLE),
        ("Overlap",        YELLOW),
    ]
    row_y = panel_y + 48
    for label, color in legend_items:
        pygame.draw.rect(win, color, (panel_x + 16, row_y, 18, 18))
        pygame.draw.rect(win, BLACK, (panel_x + 16, row_y, 18, 18), 1)
        draw_text(win, label, 18, panel_x + 44, row_y - 1, color=BLACK)
        row_y += 20


def _draw_stats(win, state, player_steps, algo_steps):
    cx = GRID_WIDTH + 225
    if state == STATE_RESULTS:
        draw_text(win, "RESULTS", 40, cx, 470, color=BLACK, center=True)
        draw_text(win, f"Player Steps:  {player_steps}", 22, GRID_WIDTH + 20, 525)
        draw_text(win, f"Optimal Steps: {algo_steps}",  22, GRID_WIDTH + 20, 555)

        if algo_steps > 0:
            # Fix #2: both player_steps and algo_steps now count edges (moves),
            # so the comparison is semantically consistent.
            match_pct = min(100, int((algo_steps / max(1, player_steps)) * 100))
            draw_text(win, f"Match: {match_pct}%", 28, cx, 600, color=BLUE, center=True)
            if match_pct >= 90:
                draw_text(win, "Excellent! 3 Stars", 28, cx, 640, color=ORANGE, center=True)
            elif match_pct >= 70:
                draw_text(win, "Good! 2 Stars",      28, cx, 640, color=ORANGE, center=True)
            else:
                draw_text(win, "Keep Trying! 1 Star",28, cx, 640, color=ORANGE, center=True)
        else:
            draw_text(win, "No path possible!", 28, cx, 600, color=RED, center=True)
    else:
        draw_text(win, "Draw path from Orange", 20, cx, 500, color=BLACK, center=True)
        draw_text(win, "Start to Cyan End",     20, cx, 525, color=BLACK, center=True)
        draw_text(win, "Then click Run Algo",   20, cx, 550, color=BLACK, center=True)
        draw_text(win, "R = Reset  |  Esc = Quit", 17, cx, 580, color=DARK_GREY, center=True)


def main():
    grid = make_grid(ROWS, GRID_WIDTH)
    start_node, end_node = apply_level(grid, "Easy", ROWS)
    current_level = "Easy"

    run   = True
    clock = pygame.time.Clock()

    # -- Map buttons (2 columns) --
    btn_easy   = Button(GRID_WIDTH + 15,  15, 200, 35, "Easy Map")
    btn_medium = Button(GRID_WIDTH + 230, 15, 200, 35, "Medium Map")
    btn_hard   = Button(GRID_WIDTH + 15,  55, 200, 35, "Hard Map")
    btn_maze   = Button(GRID_WIDTH + 230, 55, 200, 35, "Maze Map")
    btn_spiral = Button(GRID_WIDTH + 15,  95, 200, 35, "Spiral Map")
    btn_blocks = Button(GRID_WIDTH + 230, 95, 200, 35, "Blocks Map")

    # -- Algorithm buttons (full width) --
    btn_astar    = Button(GRID_WIDTH + 15, 150, 415, 35, "A* Algo",             color=LIGHT_GREEN)
    btn_dijkstra = Button(GRID_WIDTH + 15, 190, 415, 35, "Dijkstra")
    btn_bfs      = Button(GRID_WIDTH + 15, 230, 415, 35, "BFS")
    btn_dfs      = Button(GRID_WIDTH + 15, 270, 415, 35, "DFS")
    btn_greedy   = Button(GRID_WIDTH + 15, 310, 415, 35, "Greedy Best-First")
    btn_bidir    = Button(GRID_WIDTH + 15, 350, 415, 35, "Bidirectional Search")
    btn_jps      = Button(GRID_WIDTH + 15, 390, 415, 35, "Jump Point Search")
    btn_color_info = Button(GRID_WIDTH + 335, 430, 95, 32, "i Colors", font_size=20)

    # -- Action buttons --
    btn_reset  = Button(GRID_WIDTH + 15, HEIGHT - 110, 415, 40, "Reset Grid",   color=ORANGE)
    btn_submit = Button(GRID_WIDTH + 15, HEIGHT - 60,  415, 40, "Run Algorithm", color=GREEN)

    algo_buttons = {
        "A*":            btn_astar,
        "Dijkstra":      btn_dijkstra,
        "BFS":           btn_bfs,
        "DFS":           btn_dfs,
        "Greedy":        btn_greedy,
        "Bidirectional": btn_bidir,
        "JPS":           btn_jps,
    }

    selected_algo  = "A*"
    player_path    = [start_node]
    player_finished = False
    algo_path      = []
    player_steps   = 0
    algo_steps     = 0
    show_color_info = False
    state          = STATE_DRAWING

    def reset_level():
        nonlocal start_node, end_node, player_path, player_finished, state
        start_node, end_node = apply_level(grid, current_level, ROWS)
        player_path    = [start_node]
        player_finished = False
        state          = STATE_DRAWING

    # -- algo draw callback: Fix #16: redraws the full grid + sidebar each step --
    def algo_draw():
        WIN.fill(WHITE)
        pygame.draw.rect(WIN, LIGHT_BLUE, (GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
        draw_grid(WIN, grid, ROWS, GRID_WIDTH)
        pygame.display.update()

    while run:
        clock.tick(FPS)

        # Highlight selected algorithm button
        for name, btn in algo_buttons.items():
            btn.color = LIGHT_GREEN if name == selected_algo else WHITE

        all_buttons = [
            btn_easy, btn_medium, btn_hard, btn_maze, btn_spiral, btn_blocks,
            btn_astar, btn_dijkstra, btn_bfs, btn_dfs, btn_greedy, btn_bidir, btn_jps,
            btn_color_info, btn_reset,
        ]
        if player_finished:
            all_buttons.append(btn_submit)

        full_draw(WIN, grid, ROWS, all_buttons, selected_algo,
                  state, player_finished, show_color_info,
                  player_steps, algo_steps)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # -- Fix #17: keyboard shortcuts --
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_r:
                    reset_level()

            # -- UI button handling --
            if state in (STATE_DRAWING, STATE_RESULTS):
                level_map = {
                    btn_easy:   "Easy",
                    btn_medium: "Medium",
                    btn_hard:   "Hard",
                    btn_maze:   "Maze",
                    btn_spiral: "Spiral",
                    btn_blocks: "Blocks",
                }
                for btn, level_name in level_map.items():
                    if btn.handle_event(event):
                        current_level = level_name
                        reset_level()

                for name, btn in algo_buttons.items():
                    if btn.handle_event(event):
                        selected_algo = name

                if btn_color_info.handle_event(event):
                    show_color_info = not show_color_info

                if btn_reset.handle_event(event):
                    reset_level()

                if player_finished and btn_submit.handle_event(event):
                    state = STATE_RUNNING_ALGO

                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # Clear player path visually before running algo
                    for node in player_path:
                        if node != start_node and node != end_node:
                            node.reset()

                    algo_fn_map = {
                        "A*":            a_star,
                        "Dijkstra":      dijkstra,
                        "BFS":           bfs,
                        "DFS":           dfs,
                        "Greedy":        greedy_best_first,
                        "Bidirectional": bidirectional_search,
                        "JPS":           jump_point_search,
                    }
                    fn = algo_fn_map.get(selected_algo)
                    algo_path = fn(algo_draw, grid, start_node, end_node) if fn else None

                    # Fix #2: algo_steps counts moves (edges), not nodes.
                    # reconstruct_path now returns [start, ..., end], so len - 1 = moves.
                    algo_steps   = (len(algo_path) - 1) if algo_path else 0
                    player_steps = len(player_path) - 1  # player_path = [start, ..., end]

                    # Redraw player path on top of explored nodes
                    for node in player_path:
                        if node != start_node and node != end_node:
                            if algo_path and node in algo_path:
                                node.make_overlap()   # overlap highlight (Fix #5: no direct color assignment)
                            else:
                                node.make_player_path()

                    state = STATE_RESULTS

            # -- Fix #11: mouse-drag path drawing with gap-filling --
            if state == STATE_DRAWING and not player_finished:
                if pygame.mouse.get_pressed()[0]:   # left drag
                    pos     = pygame.mouse.get_pos()
                    clicked = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                    if clicked:
                        row, col = clicked
                        node      = grid[row][col]
                        last_node = player_path[-1]

                        if node != last_node and not node.is_wall():
                            dr = abs(node.row - last_node.row)
                            dc = abs(node.col  - last_node.col)

                            if dr + dc == 1:
                                # Normal adjacent step
                                if node not in player_path:
                                    player_path.append(node)
                                    if node == end_node:
                                        player_finished = True
                                    elif node != start_node:
                                        node.make_player_path()

                            elif dr + dc == 2 and (dr == 0 or dc == 0):
                                # Fix #11: cursor skipped exactly one cell — fill the gap
                                mid_row = (node.row + last_node.row) // 2
                                mid_col = (node.col  + last_node.col)  // 2
                                mid     = grid[mid_row][mid_col]
                                for step in (mid, node):
                                    if not step.is_wall() and step not in player_path:
                                        player_path.append(step)
                                        if step == end_node:
                                            player_finished = True
                                            break
                                        if step != start_node:
                                            step.make_player_path()

                elif pygame.mouse.get_pressed()[2]:  # right click to erase
                    pos     = pygame.mouse.get_pos()
                    clicked = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                    if clicked:
                        row, col = clicked
                        node     = grid[row][col]
                        if node in player_path and node != start_node and node != end_node:
                            idx = player_path.index(node)
                            for removed in player_path[idx:]:
                                if removed != start_node and removed != end_node:
                                    removed.reset()
                            player_path    = player_path[:idx]
                            player_finished = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
