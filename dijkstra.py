import numpy as np

class Node:
    def __init__(self, x, y, open):
        self.x = x
        self.y = y
        self.open = True
        self.done = False
        self.exit = False
        self.path = []

    def __str__(self):
        return f"{(self.x, self.y)}"


def Dijkstra(grid):
    heap = [grid[0][9]]

    while True:

        for node in heap:
            print(node)
            if node.exit:
                return node.path

            a = node.x + 1
            b = node.x - 1
            c = node.y + 1
            d = node.y - 1

            if ((a < 10 and c < 10) and (a > -1 and c > -1)):
                if not grid[a][c].done:
                    grid[a][c].done = True
                    grid[a][c].path = node.path
                    grid[a][c].path.append((node.x, node.y))
                    heap.append(grid[a][c])

            if ((a < 10 and d < 10) and (a > -1 and d > -1)):
                if not grid[a][d].done:
                    grid[a][d].done = True
                    grid[a][d].path = node.path
                    grid[a][d].path.append((node.x, node.y))
                    heap.append(grid[a][d])

            if ((b < 10 and c < 10) and (b > -1 and c > -1)):
                if not grid[b][c].done:
                    grid[b][c].done = True
                    grid[b][c].path = node.path
                    grid[b][c].path.append((node.x, node.y))
                    heap.append(grid[b][c])

            if ((b < 10 and d < 10) and (b > -1 and d > -1)):
                if not grid[b][d].done:
                    grid[b][d].done = True
                    grid[b][d].path = node.path
                    grid[b][d].path.append((node.x, node.y))
                    heap.append(grid[b][d])

            heap.remove(node)

# Create Grid
grid = []
for x in np.arange(0, 10):
    list = []
    for y in np.arange(0, 10):
        list.append(Node(x, y, True))
    grid.append(list)

# Creat Obstacles
for i in range(6, 10):
    grid[i][2].open = False

# Create Exit
grid[9][0].exit = True

# Create Start
grid[0][9].done = True

path = Dijkstra(grid)
print(path)
