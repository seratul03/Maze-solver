import numpy as np


def image_to_grid(binary_img: np.ndarray, cell_size: int = 8):
    """
    Convert binary maze image to grid representation.

    Args:
        binary_img (np.ndarray): Binary image (0 = wall, 255 = path)
        cell_size (int): Size of one grid cell in pixels

    Returns:
        grid (np.ndarray): 2D grid (0 = free, 1 = wall)
    """
    h, w = binary_img.shape
    grid_h = h // cell_size
    grid_w = w // cell_size

    grid = np.zeros((grid_h, grid_w), dtype=np.uint8)

    for i in range(grid_h):
        for j in range(grid_w):
            cell = binary_img[
                i * cell_size:(i + 1) * cell_size,
                j * cell_size:(j + 1) * cell_size
            ]
            if np.any(cell == 0):
                grid[i, j] = 1
            else:
                grid[i, j] = 0

    return grid

def find_start(grid: np.ndarray):
    """
    Find a start cell near the outer boundary (closest free cell to edge).
    """
    h, w = grid.shape

    min_dist = float("inf")
    start = None

    for i in range(h):
        for j in range(w):
            if grid[i, j] == 0:
                dist_to_edge = min(i, j, h - 1 - i, w - 1 - j)
                if dist_to_edge < min_dist:
                    min_dist = dist_to_edge
                    start = (i, j)

    if start is None:
        raise ValueError("No free cell found for start")

    return start


def find_goal(grid: np.ndarray):
    """
    Find goal near the center of the grid.
    """
    h, w = grid.shape
    center = (h // 2, w // 2)

    if grid[center] == 0:
        return center

    for radius in range(1, max(h, w)):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x, y = center[0] + dx, center[1] + dy
                if 0 <= x < h and 0 <= y < w:
                    if grid[x, y] == 0:
                        return (x, y)

    raise ValueError("No valid goal found")