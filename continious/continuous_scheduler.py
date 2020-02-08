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
        """
        Sorts agents in order of distance to exit and then steps
        """
        try:
            self.agents.sort(key=lambda x: x.dist)
        except Exception as e:
            print(e)

        for agent in self.agents:
            try:
                agent.step()
            except Exception as e:
                print(e)


            # Removes agents if they reach exit
            for exit in self.model.exits:
                x, y = exit.pos[0] * 6 + 1, exit.pos[1] * 6 + 1
                if agent.node == (x, y):
                    try:
                        agent.saved()
                    except Exception as e:
                        print(e)

    def get_agent_count(self):
        return len(self.agents)
