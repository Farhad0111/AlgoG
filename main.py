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

def get_clicked_pos(pos, rows, width):
    y, x = pos
    if y > width: # Clicked outside the grid
        return None
    row = x // (width // rows)
    col = y // (width // rows)
    return row, col

def apply_level(grid, level_name, rows):
    for row in grid:
        for node in row:
            node.reset()
            
    start_pos, end_pos, walls = load_level(level_name, rows)
    
    start_node = grid[start_pos[0]][start_pos[1]]
    end_node = grid[end_pos[0]][end_pos[1]]
    
    start_node.make_start()
    end_node.make_end()
    
    for r, c in walls:
        grid[r][c].make_wall()
        
    return start_node, end_node

def main():
    grid = make_grid(ROWS, GRID_WIDTH)
    
    start_node, end_node = apply_level(grid, "Easy", ROWS)
    current_level = "Easy"
    
    run = True
    clock = pygame.time.Clock()
    
    # UI Elements
    # UI Elements - Map Selection (2 columns with better spacing)
    btn_easy = Button(GRID_WIDTH + 15, 15, 200, 35, "Easy Map")
    btn_medium = Button(GRID_WIDTH + 230, 15, 200, 35, "Medium Map")
    btn_hard = Button(GRID_WIDTH + 15, 55, 200, 35, "Hard Map")
    btn_maze = Button(GRID_WIDTH + 230, 55, 200, 35, "Maze Map")
    btn_spiral = Button(GRID_WIDTH + 15, 95, 200, 35, "Spiral Map")
    btn_blocks = Button(GRID_WIDTH + 230, 95, 200, 35, "Blocks Map")
    
    # UI Elements - Algorithm Selection (Full width, single column)
    btn_astar = Button(GRID_WIDTH + 15, 150, 415, 35, "A* Algo", color=LIGHT_GREEN)
    btn_dijkstra = Button(GRID_WIDTH + 15, 190, 415, 35, "Dijkstra")
    btn_bfs = Button(GRID_WIDTH + 15, 230, 415, 35, "BFS")
    btn_dfs = Button(GRID_WIDTH + 15, 270, 415, 35, "DFS")
    btn_greedy = Button(GRID_WIDTH + 15, 310, 415, 35, "Greedy Best-First")
    btn_bidir = Button(GRID_WIDTH + 15, 350, 415, 35, "Bidirectional Search")
    btn_jps = Button(GRID_WIDTH + 15, 390, 415, 35, "Jump Point Search")
    
    # UI Elements - Action Buttons (Full width, bottom)
    btn_reset = Button(GRID_WIDTH + 15, HEIGHT - 110, 415, 40, "Reset Grid", color=ORANGE)
    btn_submit = Button(GRID_WIDTH + 15, HEIGHT - 60, 415, 40, "Run Algorithm", color=GREEN)

    selected_algo = "A*"
    
    player_path = [start_node]
    drawing_path = False
    player_finished = False
    
    algo_path = []
    
    match_percentage = 0
    player_steps = 0
    algo_steps = 0
    
    state = STATE_DRAWING

    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)
        
        # Draw Sidebar background
        pygame.draw.rect(WIN, LIGHT_BLUE, (GRID_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
        
        draw_grid(WIN, grid, ROWS, GRID_WIDTH)
        
        # Draw UI
        btn_easy.draw(WIN)
        btn_medium.draw(WIN)
        btn_hard.draw(WIN)
        btn_maze.draw(WIN)
        btn_spiral.draw(WIN)
        btn_blocks.draw(WIN)
        
        # Highlight selected algorithm
        btn_astar.color = LIGHT_GREEN if selected_algo == "A*" else WHITE
        btn_dijkstra.color = LIGHT_GREEN if selected_algo == "Dijkstra" else WHITE
        btn_bfs.color = LIGHT_GREEN if selected_algo == "BFS" else WHITE
        btn_dfs.color = LIGHT_GREEN if selected_algo == "DFS" else WHITE
        btn_greedy.color = LIGHT_GREEN if selected_algo == "Greedy" else WHITE
        btn_bidir.color = LIGHT_GREEN if selected_algo == "Bidirectional" else WHITE
        btn_jps.color = LIGHT_GREEN if selected_algo == "JPS" else WHITE
        
        btn_astar.draw(WIN)
        btn_dijkstra.draw(WIN)
        btn_bfs.draw(WIN)
        btn_dfs.draw(WIN)
        btn_greedy.draw(WIN)
        btn_bidir.draw(WIN)
        btn_jps.draw(WIN)
        
        btn_reset.draw(WIN)
        if player_finished:
            btn_submit.draw(WIN)
            
        # Draw stats if results are ready
        if state == STATE_RESULTS:
            draw_text(WIN, "RESULTS", 40, GRID_WIDTH + 225, 470, color=BLACK, center=True)
            draw_text(WIN, f"Player Steps: {player_steps}", 22, GRID_WIDTH + 20, 525)
            draw_text(WIN, f"Optimal Steps: {algo_steps}", 22, GRID_WIDTH + 20, 555)
            
            if algo_steps > 0:
                match_percentage = min(100, int((algo_steps / max(1, player_steps)) * 100))
                draw_text(WIN, f"Match: {match_percentage}%", 28, GRID_WIDTH + 225, 600, color=BLUE, center=True)
                
                if match_percentage >= 90:
                    draw_text(WIN, "Excellent! 3 Stars", 28, GRID_WIDTH + 225, 640, color=ORANGE, center=True)
                elif match_percentage >= 70:
                    draw_text(WIN, "Good! 2 Stars", 28, GRID_WIDTH + 225, 640, color=ORANGE, center=True)
                else:
                    draw_text(WIN, "Keep Trying! 1 Star", 28, GRID_WIDTH + 225, 640, color=ORANGE, center=True)
            else:
                 draw_text(WIN, "No path possible!", 28, GRID_WIDTH + 225, 600, color=RED, center=True)
        else:
             draw_text(WIN, "Draw path from Orange", 20, GRID_WIDTH + 225, 500, color=BLACK, center=True)
             draw_text(WIN, "Start to Cyan End", 20, GRID_WIDTH + 225, 525, color=BLACK, center=True)
             draw_text(WIN, "Then click Run Algorithm", 20, GRID_WIDTH + 225, 550, color=BLACK, center=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            # Handle UI clicks
            if state in [STATE_DRAWING, STATE_RESULTS]:
                if btn_easy.handle_event(event):
                    current_level = "Easy"
                    start_node, end_node = apply_level(grid, current_level, ROWS)
                    player_path = [start_node]
                    player_finished = False
                    state = STATE_DRAWING
                if btn_medium.handle_event(event):
                    current_level = "Medium"
                    start_node, end_node = apply_level(grid, current_level, ROWS)
                    player_path = [start_node]
                    player_finished = False
                    state = STATE_DRAWING
                if btn_hard.handle_event(event):
                    current_level = "Hard"
                    start_node, end_node = apply_level(grid, current_level, ROWS)
                    player_path = [start_node]
                    player_finished = False
                    state = STATE_DRAWING
                if btn_maze.handle_event(event):
                    current_level = "Maze"
                    start_node, end_node = apply_level(grid, current_level, ROWS)
                    player_path = [start_node]
                    player_finished = False
                    state = STATE_DRAWING
                if btn_spiral.handle_event(event):
                    current_level = "Spiral"
                    start_node, end_node = apply_level(grid, current_level, ROWS)
                    player_path = [start_node]
                    player_finished = False
                    state = STATE_DRAWING
                if btn_blocks.handle_event(event):
                    current_level = "Blocks"
                    start_node, end_node = apply_level(grid, current_level, ROWS)
                    player_path = [start_node]
                    player_finished = False
                    state = STATE_DRAWING
                    
                if btn_astar.handle_event(event):
                    selected_algo = "A*"
                if btn_dijkstra.handle_event(event):
                    selected_algo = "Dijkstra"
                if btn_bfs.handle_event(event):
                    selected_algo = "BFS"
                if btn_dfs.handle_event(event):
                    selected_algo = "DFS"
                if btn_greedy.handle_event(event):
                    selected_algo = "Greedy"
                if btn_bidir.handle_event(event):
                    selected_algo = "Bidirectional"
                if btn_jps.handle_event(event):
                    selected_algo = "JPS"
                    
                if btn_reset.handle_event(event):
                    start_node, end_node = apply_level(grid, current_level, ROWS)
                    player_path = [start_node]
                    player_finished = False
                    state = STATE_DRAWING
                    
                if player_finished and btn_submit.handle_event(event):
                    state = STATE_RUNNING_ALGO
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    # Clear player path visually to show algo
                    for node in player_path:
                        if node != start_node and node != end_node:
                            node.reset()
                            
                    # Run Algo
                    if selected_algo == "A*":
                        algo_path = a_star(lambda: pygame.display.update(), grid, start_node, end_node)
                    elif selected_algo == "Dijkstra":
                        algo_path = dijkstra(lambda: pygame.display.update(), grid, start_node, end_node)
                    elif selected_algo == "BFS":
                        algo_path = bfs(lambda: pygame.display.update(), grid, start_node, end_node)
                    elif selected_algo == "DFS":
                        algo_path = dfs(lambda: pygame.display.update(), grid, start_node, end_node)
                    elif selected_algo == "Greedy":
                        algo_path = greedy_best_first(lambda: pygame.display.update(), grid, start_node, end_node)
                    elif selected_algo == "Bidirectional":
                        algo_path = bidirectional_search(lambda: pygame.display.update(), grid, start_node, end_node)
                    elif selected_algo == "JPS":
                        algo_path = jump_point_search(lambda: pygame.display.update(), grid, start_node, end_node)
                    else:
                        algo_path = None
                    
                    if algo_path:
                        algo_steps = len(algo_path)
                    else:
                        algo_steps = 0
                        
                    player_steps = len(player_path) - 1
                    
                    # Redraw player path over explored nodes
                    for node in player_path:
                        if node != start_node and node != end_node:
                            # Check if it overlaps with optimal path
                            if algo_path and node in algo_path:
                                node.color = YELLOW # mix of player and optimal
                            else:
                                node.make_player_path()
                    
                    state = STATE_RESULTS

            if state == STATE_DRAWING and not player_finished:
                if pygame.mouse.get_pressed()[0]: # Left click
                    pos = pygame.mouse.get_pos()
                    clicked = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                    if clicked:
                        row, col = clicked
                        node = grid[row][col]
                        
                        # Validate contiguous drawing
                        last_node = player_path[-1]
                        
                        # If clicking on the next valid neighbor
                        if node != last_node and not node.is_wall():
                            # Check if it's a neighbor (4-way)
                            if abs(node.row - last_node.row) + abs(node.col - last_node.col) == 1:
                                if node not in player_path:
                                    player_path.append(node)
                                    if node == end_node:
                                        player_finished = True
                                    elif node != start_node:
                                        node.make_player_path()
                                        
                elif pygame.mouse.get_pressed()[2]: # Right click to erase
                    pos = pygame.mouse.get_pos()
                    clicked = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                    if clicked:
                        row, col = clicked
                        node = grid[row][col]
                        if node in player_path and node != start_node and node != end_node:
                            # Revert path up to this point
                            idx = player_path.index(node)
                            for removed_node in player_path[idx:]:
                                if removed_node != start_node and removed_node != end_node:
                                    removed_node.reset()
                            player_path = player_path[:idx]
                            player_finished = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
