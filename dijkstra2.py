import numpy as np
import copy

class Path:
    def __init__(self, node):
        pos = (node.x, node.y)
        self.path = [pos]
        self.weight = node.weight
    
    def add_node(self, node):
        pos = (node.x, node.y)
        self.path.append(pos)
        self.weight += node.weight
    def neighbours(self):
        x, y = self.path[-1]
        return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]


def Dijkstra(maingrid, pos):
    grid = copy.deepcopy(maingrid)
    ymax, xmax = len(grid[0]), len(grid)
    x, y = pos
    stack = [Path(grid[x][y])]
    while True:
        min_weigth = min([x.weight for x in stack])
        heap = [x for x in stack if x.weight is min_weigth]
        stack = [x for x in stack if x not in heap]        
        for guess in heap:
            neighbours = guess.neighbours()
            for neighbour in neighbours:
                x, y = neighbour
                if x >= 0 and x < xmax and y >= 0 and y < ymax and grid[x][y].path_weight > guess.weight:
                    path = copy.deepcopy(guess)
                    grid[x][y].path_weight = path.weight
                    path.add_node(grid[x][y])
                    if grid[x][y].exit:
                        path.path = path.path[1:]
                        return path
                    stack.append(path)
