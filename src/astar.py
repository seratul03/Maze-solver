import heapq
import numpy as np


def astar_pixels(binary_img, start, goal):
    h, w = binary_img.shape
    g_cost = np.full((h, w), np.inf)
    g_cost[start] = 0

    parent = {}
    visited = set()
    order = []

    def h_cost(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    pq = [(h_cost(start, goal), start)]

    while pq:
        _, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        order.append(current)

        if current == goal:
            break

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < h and 0 <= ny < w:
                if binary_img[nx, ny] != 255:
                    continue

                new_g = g_cost[current] + 1
                if new_g < g_cost[nx, ny]:
                    g_cost[nx, ny] = new_g
                    parent[(nx, ny)] = current
                    f = new_g + h_cost((nx, ny), goal)
                    heapq.heappush(pq, (f, (nx, ny)))

    if goal not in parent:
        return None, order

    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.append(start)

    return path[::-1], order