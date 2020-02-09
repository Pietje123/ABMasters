from mesa import Agent
import random
import numpy as np
from discrete.dijkstra_weigths import *

class Node:
    """
    Node for the discrete grid used for pathfinding with Dijkstra's algorithm.

    Attributes:
    self.x : x-position in grid (Int)
    self.y : y-position in grid (Int)
    self.done : check whether this node should be considered (Boolean)
    self.exit : check whether node is an exit (Boolean)
    self.weight : weight of the grid tile (Float)
    self.path_weight : total weight to move to this tile for an agent (Float)

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.done = False
        self.exit = False
        self.weight = 1
        self.path_weight = np.inf

    def __str__(self):
        return f"{(self.x, self.y)}"

class Objects(Agent):
    """
    Parent object for all agents (inherits from Mesa Agent).
    self.pos : current position of agent (Tuple)
    self.model : the model (MesaModel)
    """
    def __init__(self, model, pos, weight):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.model = model
        self.weight = weight
        x, y = pos
        self.model.floorplan[x][y].weight = weight

    # if an object is moved, the weigths of the floorplan need to be updated
    def update_floorplan(self):
        floorplan = self.model.floorplan
        floorplan[self.pos[0]][self.pos[1]].weight =1
        floorplan[self.new_pos[0]][self.new_pos[1]].weight = self.weight

    def get_position(self):
        return self.pos


class Furniture(Objects):
    def __init__(self, model, pos, weight):
        super().__init__(model, pos, weight)

class Wall(Objects):
    def __init__(self, model, pos, weight):
        super().__init__(model, pos, weight)

class Exit(Objects):
    def __init__(self, model, pos, weight):
        super().__init__(model, pos, weight)

class Human(Objects):
    """
    Human agents in the simulation

    self.path : shortest path to exit (List)
    self.speed : current speed of agent (Int)
    self.max_speed : maximum speed of agent (Int)
    self.panic : chance to stray from path (Floar)
    """
    def __init__(self, model, pos, weight, panic = 0, max_speed = 3):
        super().__init__(model, pos, weight)
        getattr(model, f'schedule_{self.__class__.__name__}').add(self)
        self.path = self.dijkstra()
        self.speed = 1
        self.max_speed = max_speed
        self.panic = random.random() * panic if panic < 1 else random.random()

    def dijkstra(self):
        """
        Find new shortest path and update in the agent
        """
        self.path = Dijkstra(self.model.floorplan, self.pos)
        self.new_pos = self.path.path[0]
        self.dist = len(self.path.path)

    def step(self):
        """
        Executes all methods for 1 simulation step in the right order.
        
        """

        # run i tiles
        for i in range(self.speed):

            # calculate shortest path 
            self.dijkstra()

            # get free neighbouring cells
            other_free_cells = list(set(self.model.grid.get_free_cells(self.pos)) - set([self.new_pos]))

            # chance to panic and chekc if possible to stray from path
            if random.random() < self.panic and other_free_cells:
                self.new_pos = random.choice(other_free_cells)

            # check if next tile is empty, if so move there
            if self.model.grid.is_cell_empty(self.new_pos):
                self.update_floorplan()
                self.model.grid.move_agent(self, self.new_pos)
                if self.speed < self.max_speed:
                    self.speed += 1
            else:
                self.speed = 1

            # check if agent is saved
            if self.new_pos in self.model.exits:
                self.saved()
                break



    def saved(self):
        """
        Removes agent from Mesa Model.
        """
        self.model.remove_agent(self)

