from src.image_loader import load_image
from src.preprocess import binarize_image
from src.bfs import bfs_pixels
from src.astar import astar_pixels

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

IMAGE_PATH = "data/raw/maze.png"


def find_start_pixel(binary):
    h, w = binary.shape
    best, pos = 1e9, None
    for i in range(h):
        for j in range(w):
            if binary[i, j] == 255:
                d = min(i, j, h - 1 - i, w - 1 - j)
                if d < best:
                    best, pos = d, (i, j)
    return pos


def find_goal_pixel(binary):
    h, w = binary.shape
    cx, cy = h // 2, w // 2
    best, pos = 1e9, None
    for i in range(h):
        for j in range(w):
            if binary[i, j] == 255:
                d = abs(i - cx) + abs(j - cy)
                if d < best:
                    best, pos = d, (i, j)
    return pos


def animate(order, path, binary, title, color):
    canvas = np.dstack([binary, binary, binary])
    fig, ax = plt.subplots()
    img = ax.imshow(canvas)
    ax.set_title(title)
    ax.axis("off")

    skip = 10
    interval = 0 

    def update(i):
        idx = i * skip

        if idx < len(order):
            x, y = order[idx]
            canvas[x, y] = color
        else:
            for x, y in path:
                canvas[x, y] = [0, 255, 0]

        img.set_data(canvas)
        return img,

    ani = FuncAnimation(
        fig,
        update,
        frames=len(order) // skip + 30,
        interval=interval,
        blit=True
    )

    plt.show()


def main():
    gray = load_image(IMAGE_PATH)
    binary = binarize_image(gray, invert=True)

    start = find_start_pixel(binary)
    goal = find_goal_pixel(binary)

    bfs_path, bfs_order = bfs_pixels(binary, start, goal)
    astar_path, astar_order = astar_pixels(binary, start, goal)

    animate(
        bfs_order,
        bfs_path,
        binary.copy(),
        "BFS Exploration",
        [0, 0, 255]   
    )

    animate(
        astar_order,
        astar_path,
        binary.copy(),
        "A* Exploration",
        [255, 0, 0]  
    )


if __name__ == "__main__":
    main()