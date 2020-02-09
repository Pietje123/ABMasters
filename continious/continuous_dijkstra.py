import numpy as np
import copy

def dijkstra(maingrid, pos):
    """
    Applies Dijkstra's algorithm on the input grid.
    """
    grid = copy.copy(maingrid)
    xmax, ymax = len(grid[0]), len(grid)
    xs, ys = pos[0], pos[1]
    grid[ys][xs].done = True
    stack = [grid[ys][xs]]

    # Continue search untill loop is broken by finding the exit
    while True:
        heap = stack
        stack = []
        for node in heap:
            if node.exit:
                node.path.append(node.pos)
                return node.path[1:]

            # Shorthand for coordinates
            a = node.pos[0] + 1
            b = node.pos[0] - 1
            c = node.pos[0]
            d = node.pos[1] + 1
            e = node.pos[1] - 1
            f = node.pos[1]

            # Check 4 closest nodes (Von Neumann neighborhood)
            if a > -1 and a < xmax:
                if not grid[f][a].done:
                    grid[f][a].done = True
                    grid[f][a].path = node.path.copy()
                    grid[f][a].path.append((c, f))
                    stack.append(grid[f][a])

            if b > -1 and b < xmax:
                if not grid[f][b].done:
                    grid[f][b].done = True
                    grid[f][b].path = node.path.copy()
                    grid[f][b].path.append((c, f))
                    stack.append(grid[f][b])

            if d > -1 and d < ymax:
                if not grid[d][c].done:
                    grid[d][c].done = True
                    grid[d][c].path = node.path.copy()
                    grid[d][c].path.append((c, f))
                    stack.append(grid[d][c])

            if e > -1 and e < ymax:
                if not grid[e][c].done:
                    grid[e][c].done = True
                    grid[e][c].path = node.path.copy()
                    grid[e][c].path.append((c, f))
                    stack.append(grid[e][c])
