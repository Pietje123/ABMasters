import numpy as np
import random as rnd

class DistanceScheduler:
    def __init__(self):
        self.steps = 0
        self.agents = []

    def add(self, agent):
        self.agents.append(agent)

    def remove(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)

    def step(self):
        for agent in rnd.shuffle(self.agents).sort(key=lambda x: x.dist):
            print(agent)
            agent.step()
