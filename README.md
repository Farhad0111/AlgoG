# AlgoG - Pathfinding Challenge

AlgoG is an interactive pathfinding visualization and puzzle game built with Python and Pygame. It allows users to manually draw paths on a grid, compare their efficiency against optimal algorithms like A* and Dijkstra, and explore various pre-designed challenge maps.

## Features

- **Interactive Grid**: Manually draw paths from start to finish.
- **Pre-designed Maps**: Choose from various maps including Easy, Medium, Hard, Maze, Spiral, and Blocks.
- **Pathfinding Algorithms**: Compare your results with industry-standard algorithms:
  - **A* Search**: Uses heuristics to find the shortest path efficiently.
  - **Dijkstra's Algorithm**: Guarantees the shortest path by exploring all possible directions.
- **Performance Metrics**: Compare your path steps against the algorithm's optimal steps.
- **Customizable Environment**: Easy to add or edit maps in `levels.py`.

## Project Structure

- `main.py`: The entry point of the application. Handles the game loop, user input, and UI rendering.
- `algorithms.py`: Contains the implementations of the A* and Dijkstra pathfinding algorithms.
- `grid.py`: Handles grid creation, node management, and drawing.
- `levels.py`: Stores the map layouts and includes a parser to load them into the grid.
- `ui.py`: Contains UI components like buttons and text drawing functions.
- `constants.py`: Centralized file for colors, dimensions, and game states.
- `requirements.txt`: Lists the dependencies required to run the project.

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
