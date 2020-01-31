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
        self.new_pos = totalforce(self.pos, self.path[0], self.model.humans)
        print(f"Pos: {self.pos}, Target: {self.new_pos}")
        print(f"Node: {self.node}, Path: {self.path}")

    def get_node(self):
        xs, ys = self.pos
        self.node = int(np.round(xs * 3)), int(np.round(ys * 3))
        # dist = np.sqrt((xe / 3 - xs)**2 + (ye / 3 - ys)**2)
        # if dist < 0.16666 and len(self.path) != 0:
        #     self.node = self.path[0]

    def move(self):
        try:
            self.model.space.move_agent(self, self.new_pos)
        except:
            pass

    def step(self):
        try:
            self.dijkstra()
            self.get_node()
            self.force()
            self.move()
        except Exception as e:
            pass

    def saved(self):
        self.model.remove_agent(self)
