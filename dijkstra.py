import numpy as np

class Node:
    def __init__(self, x, y, open):
        self.x = x
        self.y = y
        self.done = False
        self.exit = False
        self.path = []

    def __str__(self):
        return f"{(self.x, self.y)}"


def Dijkstra(grid):
    stack = [grid[0][9]]

    while True:
        heap = stack
        stack = []
        for node in heap:
            if node.exit:
                return node.path

            a = node.x + 1
            b = node.x - 1
            c = node.x
            d = node.y + 1
            e = node.y - 1
            f = node.y

            if a > -1 and a < 10:
                if not grid[a][f].done:
                    grid[a][f].done = True
                    grid[a][f].path = node.path.copy()
                    grid[a][f].path.append((c, f))
                    stack.append(grid[a][f])

            if b > -1 and b < 10:
                if not grid[b][f].done:
                    grid[b][f].done = True
                    grid[b][f].path = node.path.copy()
                    grid[b][f].path.append((c, f))
                    stack.append(grid[b][f])

            if d > -1 and d < 10:
                if not grid[c][d].done:
                    grid[c][d].done = True
                    grid[c][d].path = node.path.copy()
                    grid[c][d].path.append((c, f))
                    stack.append(grid[c][d])

            if e > -1 and e < 10:
                if not grid[c][e].done:
                    grid[c][e].done = True
                    grid[c][e].path = node.path.copy()
                    grid[c][e].path.append((c, f))
                    stack.append(grid[c][e])

# Create Grid
grid = []
for x in np.arange(0, 10):
    list = []
    for y in np.arange(0, 10):
        list.append(Node(x, y, True))
    grid.append(list)

# Creat Obstacles
for i in range(2, 10):
    grid[i][2].done = True

for i in range(1, 9):
    grid[i][6].done = True

for i in range(0, 4):
    grid[i][8].done = True

# Create Exit
grid[9][0].exit = True

# Create Start
grid[0][9].done = True

path = Dijkstra(grid)
print(path)
