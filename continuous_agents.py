from mesa import Agent
import numpy as np
from continuous_dijkstra import dijkstra
from continuous_forces import totalforce

class Node:
    def __init__(self, position):
        self.pos = position
        self.done = False
        self.exit = False
        self.path = []

    def __str__(self):
        x, y = self.pos
        return f"{x / 3, y / 3}"

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
        getattr(model, f'scheduler').add(self)
        self.new_pos = 0
        self.path = []
        self.node = 3 * self.pos[0], 3 * self.pos[1]

    def dijkstra(self):
        self.path = dijkstra(self.model.grid, self.node)

    def force(self):
        self.new_pos = totalforce(self.pos, self.node, self.model.humans)

    def get_node(self):
        xs, ys = self.pos
        xe, ye = self.path[0]
        dist = np.sqrt((xe / 3 - xs)**2 + (ye / 3 - ys)**2)
        print(dist)
        if dist < 0.2:
            self.node = self.path[0]

    def move(self):
        self.model.space.move_agent(self, self.new_pos)

    def step(self):
        self.dijkstra()
        self.get_node()
        self.force()
        self.move()

    def saved(self):
        self.model.remove_agent(self)
