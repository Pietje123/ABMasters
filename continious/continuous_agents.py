import numpy as np
from mesa import Agent

from continuous_dijkstra import dijkstra
from continuous_forces import totalforce

class Node:
    """
    Node for the discrete grid used for pathfinding with Dijkstra's algorithm.

    Attributes:
    self.pos : position in grid (tuple)
    self.done : check whether this node should be considered (Boolean)
    self.exit : check whether node is an exit (Boolean)
    self.path : current shortest path to node
    """
    def __init__(self, position):
        self.pos = position
        self.done = False
        self.exit = False
        self.path = []

    def __str__(self):
        x, y = self.pos
        return f"{x / 6, y / 6}"

class Objects(Agent):
    """
    Parent object for all agents (inherits from Mesa Agent).
    """
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.model = model

    def get_position(self):
        return self.pos

class Furniture(Objects):
    def __init__(self, model, pos):
        super().__init__(model, pos)

class Wall(Objects):
    def __init__(self, model, pos):
        super().__init__(model, pos)

class Exit(Objects):
    def __init__(self, model, pos):
        super().__init__(model, pos)

class Human(Objects):
    """
    Human agents in simulation.

    Attributes:
    self.new_pos : specified movement target (tuple)
    self.node : closest node in grid
    self.path : current shortest path to exit
    self.dist : lenght of current shortest path
    """
    def __init__(self, model, pos):
        super().__init__(model, pos)
        getattr(model, f'scheduler').add(self)
        self.new_pos = 0
        self.node = 6 * self.pos[0], 6 * self.pos[1]
        self.path = dijkstra(self.model.grid, self.node)
        self.dist = len(self.path)

    def dijkstra(self):
        """
        Pathfinding algorithm, calculates path & distance.
        """
        self.path = dijkstra(self.model.grid, self.node)
        self.dist = len(self.path)

    def force(self):
        """
        Calculates forces from Social Force Model (currently only self-driving
        force and human-human interactions).
        """
        self.new_pos = totalforce(self.pos, self.path[0], self.model.humans)

    def get_node(self):
        """
        Finds closest node in grid.
        """
        xs, ys = self.pos
        self.node = int(np.round(xs * 6)), int(np.round(ys * 6))

    def move(self):
        """
        Moves agent in Mesa ContinuousSpace.
        """
        self.model.space.move_agent(self, self.new_pos)

    def step(self):
        """
        Executes all methods for 1 simulation step in the right order.
        Currently uses try/Except as failsafe.
        """
        try:
            self.dijkstra()
            self.get_node()
            self.force()
            self.move()
        except Exception as e:
            print(e)

    def saved(self):
        """
        Removes agent from Mesa class ContinuousSpace.
        """
        self.model.remove_agent(self)
