import numpy as np
import random as rnd

class DistanceScheduler:
    """
    Scheduler that activates agents in order of path-to-exit distance. Closest
    agents are activated first to maximize flow through exit.
    """
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
        for agent in sorted(self.agents, key=lambda x: x.dist):
            agent.step()
        self.steps += 1

    def get_agent_count(self):
        return len(self.agents)

    def get_steps(self):
        return self.steps
