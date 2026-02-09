This project is a Python-based application designed to generate polar mazes and solve them using pathfinding algorithms like Breadth-First Search (BFS) and A* Search.

#### Features

* **Maze Generation**: Creates circular (polar) mazes using a Recursive Backtracker algorithm and saves them as high-resolution images.
* **Verification**: Includes a built-in verification step to ensure a valid path exists from the outer rim to the center before saving.
* **Pathfinding Algorithms**: Implements both BFS and A* Search to find the shortest path through the maze.
* **Visual Animation**: Uses Matplotlib to animate the exploration process of each algorithm and highlight the final path.
* **Customizable Parameters**: Allows users to configure maze dimensions, pathfinding algorithms, and visualization settings.
* **Error Handling**: Provides robust error handling for invalid image paths and corrupted files.

#### Project Structure

* `main.py`: The entry point for running the maze solver and visualizer.
* `src/`: Contains core logic modules:
  * `astar.py`: Implementation of the A* pathfinding algorithm.
  * `bfs.py`: Implementation of the BFS pathfinding algorithm.
  * `create_maze.py`: Logic for generating and saving polar mazes.
  * `grid_utils.py`: Utilities for converting images to grid representations and identifying start/goal points.
  * `image_loader.py`: Handles loading and converting maze images to grayscale.
  * `preprocess.py`: Binarizes images for processing.
  * `visualize.py`: Placeholder for visualization utilities (currently empty).

* `data/`: Contains maze image data:
  * `raw/`: Directory where generated maze images are stored.
  * `processed/`: Directory for processed maze grids.

#### Usage

1. **Generate a Maze**:
   ```bash
   python -m src.create_maze
   ```
   This will generate a polar maze and save it in the `data/raw/` directory.

2. **Solve a Maze**:
   - Update the `IMAGE_PATH` variable in `main.py` to point to the desired maze image.
   - Run the solver:
     ```bash
     python main.py
     ```

3. **Customize Parameters**:
   - Modify the `rings` and `sectors` parameters in `src/create_maze.py` to adjust maze dimensions.
   - Choose between BFS and A* algorithms in `main.py`.

4. **Visualize the Solution**:
   - The solution path and exploration process will be animated using Matplotlib.

#### Requirements

Ensure you have the required Python packages installed:
```bash
pip install -r requirements.txt
```

#### Contributing

Feel free to submit issues or pull requests to improve the project. Contributions are welcome!