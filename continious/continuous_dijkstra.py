import numpy as np
import copy

def dijkstra(maingrid, pos):

    grid = copy.deepcopy(maingrid)
    ymax, xmax = len(grid[0]), len(grid)
    xs, ys = pos[0], pos[1]
    stack = [grid[ys][xs]]

    while True:
        heap = stack
        stack = []
        for node in heap:
            if node.exit:
                node.path.append(node.pos)
                return node.path[1:]

            a = node.pos[0] + 1
            b = node.pos[0] - 1
            c = node.pos[0]
            d = node.pos[1] + 1
            e = node.pos[1] - 1
            f = node.pos[1]

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
