from collections import deque
import numpy as np


def bfs_pixels(binary_img, start, goal):
    h, w = binary_img.shape
    visited = np.zeros((h, w), dtype=bool)
    parent = {}
    order = []

    q = deque([start])
    visited[start] = True
    parent[start] = None

    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    while q:
        x, y = q.popleft()
        order.append((x, y))

        if (x, y) == goal:
            break

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w:
                if not visited[nx, ny] and binary_img[nx, ny] == 255:
                    visited[nx, ny] = True
                    parent[(nx, ny)] = (x, y)
                    q.append((nx, ny))

    if goal not in parent:
        return None, order

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    return path[::-1], order