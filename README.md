# AlgoG - Pathfinding Challenge

AlgoG is an interactive pathfinding visualization and puzzle game built with Python and Pygame. It allows users to manually draw paths on a grid, compare their efficiency against optimal algorithms like A* and Dijkstra, and explore various pre-designed challenge maps.

## Features

- **Interactive Grid**: Manually draw paths from start to finish.
- **Pre-designed Maps**: Choose from various maps including Easy, Medium, Hard, Maze, Spiral, and Blocks.
- **Pathfinding Algorithms**: Compare your results with industry-standard algorithms:
  - **A* Search**: Uses heuristics to find the shortest path efficiently.
  - **Dijkstra's Algorithm**: Guarantees the shortest path by exploring all possible directions.
  - **BFS (Breadth-First Search)**: Explores uniformly in all directions.
  - **DFS (Depth-First Search)**: Prioritizes depth over area.
  - **Greedy Best-First Search**: Chases the goal using only a heuristic.
  - **Bidirectional Search**: Searches from both start and end simultaneously.
  - **Jump Point Search (JPS)**: Optimized for uniform-cost grids to skip unnecessary nodes.
- **Performance Metrics**: Compare your path steps against the algorithm's optimal steps.
- **Customizable Environment**: Easy to add or edit maps in `levels.py`.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AlgoG.git
   cd AlgoG
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
python main.py
```

## How to Play

1. **Select a Map**: Choose a level from the sidebar.
2. **Select an Algorithm**: Choose which algorithm you want to compete against.
3. **Draw Your Path**: Click and drag your mouse from the **Start** (Orange) to the **End** (Cyan) to draw your path.
4. **Run Algorithm**: Click "Run Algorithm" to see how the selected AI finds the path.
5. **Compare**: View the step count comparison in the sidebar results.
6. **Reset**: Click "Reset Application" to clear the board or "Clear Paths" to try again on the same map.

## Project Structure

- `main.py`: The entry point of the application. Handles the game loop, user input, and UI rendering.
- `algorithms.py`: Contains the implementations of the A* and Dijkstra pathfinding algorithms.
- `grid.py`: Handles grid creation, node management, and drawing.
- `levels.py`: Stores the map layouts and includes a parser to load them into the grid.
- `ui.py`: Contains UI components like buttons and text drawing functions.
- `constants.py`: Centralized file for colors, dimensions, and game states.
- `requirements.txt`: Lists the dependencies required to run the project.

## Pathfinding Algorithms Overview

1.  **Breadth-First Search (BFS)**
    - **How it behaves**: BFS explores uniformly in all directions, layer by layer, like a ripple in a pond. Starting at the Orange square, it will flood the empty space. It will hit the immediate vertical walls, wrap around their top and bottom openings, and slowly fill the entire left side of the map—including wasting time exploring every nook of that zig-zag wall on the bottom left.
2.  **Depth-First Search (DFS)**
    - **How it behaves**: DFS prioritizes depth over area, plunging blindly in one directional priority (e.g., always trying Up, then Right, then Down, then Left) until it hits a wall, then backtracking.
3.  **Dijkstra’s Algorithm**
    - **How it behaves**: Because this grid map is unweighted (moving from one tile to any adjacent tile has an identical cost of 1), Dijkstra behaves exactly like BFS.
4.  **Greedy Best-First Search**
    - **How it behaves**: This algorithm relies entirely on a heuristic—typically the straight-line (Euclidean or Manhattan) distance to the goal—ignoring how much distance it has already traveled. From the Orange square, it wants to rush directly up and right toward the Cyan square.
5.  **A* Search (A-Star)**
    - **How it behaves**: A* balances both worlds using the evaluation function $f(n) = g(n) + h(n)$, where $g(n)$ is the actual path cost from the start and $h(n)$ is the estimated distance to the goal.
6.  **Bidirectional Search**
    - **How it behaves**: This approach runs two simultaneous searches: one forward from the Orange square and one backward from the Cyan square, stopping when the two frontiers meet in the middle.
7.  **Jump Point Search (JPS)**
    - **How it behaves**: JPS is a highly specialized optimization of A* designed specifically for uniform-cost grids like this one. Instead of evaluating every single open neighbor cell by cell, it looks ahead along straight horizontal, vertical, and diagonal lines to find "jump points"—essentially corners or edges of obstacles that force a change in direction.

### Real-World Speed Ranking (Typical)

For large grid maps:

Fastest → Slowest
1. **JPS**
2. **Bidirectional A***
3. **A***
4. **Greedy Best-First**
5. **BFS**
6. **Dijkstra**
7. **DFS** (unreliable)

### Memory Usage Ranking

Lowest → Highest
1. **DFS**
2. **Greedy**
3. **A***
4. **JPS**
5. **BFS**
6. **Dijkstra**

### Comparison Table
----------------------------------------------------------------------------------------------------------------------------------------------------------
| Algorithm                  | Time Complexity              | Space Complexity      | Optimal?                | Complete?  | Main Idea                   |
| -------------------------- | ---------------------------- | --------------------- | ----------------------- | ---------- | --------------------------- |
| Breadth-First Search (BFS) | $O(V + E)$                   | $O(V)$                | Yes (unweighted)        | Yes        | Expands layer by layer      |
| Depth-First Search (DFS)   | $O(V + E)$                   | $O(V)$                | No                      | Sometimes  | Goes deep first             |
| Dijkstra                   | $O((V+E)\log V)$             | $O(V)$                | Yes                     | Yes        | Expands lowest cost         |
| Greedy Best-First          | Worst: $O(V)$ to $O(E)$      | $O(V)$                | No                      | Not always | Chases goal using heuristic |
| A*                         | Worst: like Dijkstra         | $O(V)$                | Yes (good heuristic)    | Yes        | Combines cost + heuristic   |
| Bidirectional Search       | Roughly $O(b^{d/2})$         | $O(b^{d/2})$          | Yes (with BFS/Dijkstra) | Yes        | Searches from both ends     |
| Jump Point Search (JPS)    | Much faster than A* on grids | Lower than A* usually | Yes                     | Yes        | Skips unnecessary nodes     |
----------------------------------------------------------------------------------------------------------------------------------------------------------

### Symbol Meanings
-------------------------------------------------------
| Symbol | Meaning                                    |
| ------ | ------------------------------------------ |
| $V$    | Number of vertices (cells/nodes)           |
| $E$    | Number of edges (connections)              |
| $b$    | Branching factor (possible moves per step) |
| $d$    | Depth / distance to goal                   |
-------------------------------------------------------

## Map Legend

- `.` : Empty passable cell
- `W` : Wall (impassable)
- `S` : Start Node (Green)
- `E` : End Node (Red)

## Color Legend

- `WHITE` : Empty / passable cell
- `BLACK` : Wall / impassable block
- `ORANGE` : Start node
- `TURQUOISE` : End node
- `PURPLE` : Player-drawn path
- `BLUE` : Algorithm path result
- `GREEN` : Open nodes being considered by the algorithm
- `RED` : Closed nodes already evaluated by the algorithm

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AlgoG
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Select a Map**: Click on the map buttons in the sidebar (Easy, Medium, Hard, etc.) to load a layout.
3. **Select an Algorithm**: Choose between "A* Algo" and "Dijkstra".
4. **Draw Your Path**: Click and drag on the grid to draw what you think is the shortest path.
5. **Run Algorithm**: Click "Run Algorithm" to see the optimal path calculated by the computer.
6. **Reset**: Use "Reset Grid" to clear the current path and try again.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
