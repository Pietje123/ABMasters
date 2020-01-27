from mesa import Agent
import random
import numpy as np
from dijkstra import *

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.done = False
        self.exit = False
        self.path = []

    def __str__(self):
        return f"{(self.x, self.y)}"

class Objects(Agent):
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
    def __init__(self, model, pos):
        super().__init__(model, pos)
        getattr(model, f'schedule_{self.__class__.__name__}').add(self)
        self.new_pos = 0
        self.path = Dijkstra(self.model.floorplan, self.pos)
        self.dist = len(self.path)

    def dijkstra(self):
        self.path = Dijkstra(self.model.floorplan, self.pos)
        self.dist = len(self.path)

    def move(self):
        self.new_pos = self.path[0]
        self.path = self.path[1:]

    def step(self):
        self.move()
        self.advance()
        self.dijkstra()

    def saved(self):
        self.model.remove_agent(self)

    def advance(self):
        self.model.grid.move_agent(self, self.new_pos)
