import numpy as np
import copy

class Path:
    """
    Path for discrete grid for the weighted dijkstra

    self.path : list of nodes (List)
    self.weight : weigth of current path (Float)
    """
    def __init__(self, node):
        pos = (node.x, node.y)
        self.path = [pos]
        self.weight = node.weight
    
    def add_node(self, node):
        pos = (node.x, node.y)
        self.path.append(pos)
        self.weight += node.weight
    

    def neighbours(self):
        """
        Returns the adjecent tiles of the current end point
        """
        x, y = self.path[-1]
        return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]


def Dijkstra(maingrid, pos):
    """
    Dijkstra algorithm with weigths
    """

    grid = copy.deepcopy(maingrid)
    ymax, xmax = len(grid[0]), len(grid)
    x, y = pos
    stack = [Path(grid[x][y])]

    # continue until exit is found
    while True:

        # get lightest paths 
        min_weigth = min([x.weight for x in stack])
        heap = [x for x in stack if x.weight is min_weigth]

        # remove lightest paths from all paths
        stack = [x for x in stack if x not in heap]

        for guess in heap:
            neighbours = guess.neighbours()

            # check all adjacent tiles
            for neighbour in neighbours:
                x, y = neighbour

                # check boundary conditions
                # and check if this path is the lightest to that tile
                if x >= 0 and x < xmax and y >= 0 and y < ymax and grid[x][y].path_weight > guess.weight:
                    path = copy.deepcopy(guess)
                    grid[x][y].path_weight = path.weight
                    path.add_node(grid[x][y])

                    # return path if exit is found
                    if grid[x][y].exit:
                        path.path = path.path[1:]
                        return path
                    stack.append(path)
