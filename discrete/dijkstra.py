import numpy as np
import copy

def Dijkstra(maingrid, pos):

    grid = copy.deepcopy(maingrid)
    ymax, xmax = len(grid[0]), len(grid)
    x, y = pos
    stack = [grid[x][y]]

    while True:
        heap = stack
        stack = []
        for node in heap:
            if node.exit:
                node.path.append((node.x, node.y))
                return node.path[1:]

            a = node.x + 1
            b = node.x - 1
            c = node.x
            d = node.y + 1
            e = node.y - 1
            f = node.y

            if a > -1 and a < xmax:
                if not grid[a][f].done:
                    grid[a][f].done = True
                    grid[a][f].path = node.path.copy()
                    grid[a][f].path.append((c, f))
                    stack.append(grid[a][f])

            if b > -1 and b < xmax:
                if not grid[b][f].done:
                    grid[b][f].done = True
                    grid[b][f].path = node.path.copy()
                    grid[b][f].path.append((c, f))
                    stack.append(grid[b][f])

            if d > -1 and d < ymax:
                if not grid[c][d].done:
                    grid[c][d].done = True
                    grid[c][d].path = node.path.copy()
                    grid[c][d].path.append((c, f))
                    stack.append(grid[c][d])

            if e > -1 and e < ymax:
                if not grid[c][e].done:
                    grid[c][e].done = True
                    grid[c][e].path = node.path.copy()
                    grid[c][e].path.append((c, f))
                    stack.append(grid[c][e])
