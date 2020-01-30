import numpy as np
import random as rnd

class DistanceScheduler:
    def __init__(self, model):
        self.steps = 0
        self.agents = []
        self.model = model

    def add(self, agent):
        self.agents.append(agent)

    def remove(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)

    def step(self):
        counter = 1
        rnd.shuffle(self.agents)
        for agent in self.agents:
            agent.step()
            print(f"Agent {counter} of {len(self.agents)}")
            counter += 1
            if agent.pos in self.model.exits:
                agent.saved()

    def get_agent_count(self):
        return len(self.agents)
