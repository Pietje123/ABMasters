from mesa import Agent
import random
import numpy as np
from dijkstra2 import *

class Node:
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
        self.path = Dijkstra(self.model.floorplan, self.pos)
        self.dist = self.path.weight
        self.new_pos = self.path.path[0]
        self.pos = pos
        self.speed = 1
        self.max_speed = 3
        self.panic = random.random() * 0

    def dijkstra(self):
        self.path = Dijkstra(self.model.floorplan, self.pos)
        self.new_pos = self.path.path[0]
        self.dist = self.path.weight

    def step(self):
        for i in range(self.speed):
            self.dijkstra()
            other_free_cells = list(set(self.model.grid.get_free_cells(self.pos)) - set([self.new_pos]))

            if random.random() < self.panic and other_free_cells:
                self.new_pos = random.choice(other_free_cells)

            if self.model.grid.is_cell_empty(self.new_pos):

                self.model.grid.move_agent(self, self.new_pos)
                if self.speed < self.max_speed:
                    self.speed += 1
            else:
                self.speed = 1

            if self.new_pos in self.model.exits:
                self.saved()
                break


    def saved(self):
        self.model.remove_agent(self)

