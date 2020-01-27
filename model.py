from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
import os
import numpy as np
from agents import *
from scheduler import DistanceScheduler

class Classroom(Model):
	def __init__(self, floorplan):
		super().__init__()
		self.n_agents = 0
		self.agents = []
		self.schedules = ['Human']
		self.schedule_Human = DistanceScheduler()
		# SimultaneousActivation(self)
		self.exits = []
		self.floorplan = []
		with open('floorplans/' + floorplan) as f:
			[self.floorplan.append(line.strip().split()) for line in f.readlines()]

		size = len(self.floorplan) , len(self.floorplan[0])
		self.grid = MultiGrid(size[0], size[1], torus=False)

		for i in range(size[0]):
			for j in range(size[1]):
				value = str(self.floorplan[i][j])
				self.floorplan[i][j] = Node(i,j)
				if value == 'W':
					self.new_agent(Wall, (i,j))
					self.floorplan[i][j].done = True

				elif value == 'F':
					self.floorplan[i][j].done = True
					self.new_agent(Furniture, (i,j))

				elif value == 'S':
					self.new_agent(Human, (i,j))

				elif value == 'E':
					self.floorplan[i][j].exit = True
					self.new_agent(Exit, (i,j))
					self.exits.append((i, j))

		for agent in self.agents:
			agent.dijkstra()

		for agent in self.agents.


	def new_agent(self, agent_type, pos):
		'''
		Method that creates a new agent, and adds it to the correct scheduler.
		'''
		agent = agent_type(self, pos)
		self.grid.place_agent(agent, pos)
		if agent_type.__name__ in self.schedules:
			getattr(self, f'schedule_{agent_type.__name__}').add(agent)
			self.agents.append(agent)

	def remove_agent(self, agent):
		'''
		Method that removes an agent from the grid and the correct scheduler.
		'''
		self.grid.remove_agent(agent)
		getattr(self, f'schedule_{type(agent).__name__}').remove(agent)

	def step(self):
		'''
		Method that steps every agent.
		'''

		self.schedule_Human.step()

	def run_model(self):
		self.step()

print("Initialised")
tester = Classroom('floorplan_c0_110.txt')
test = tester.agents[0]
print(test.pos)
tester.step()
print(test.pos)


# tester.run_model()
# # Create a RandomWalker, so that we can call the random_move() method
# start_position = (5, 5)
# tester.new_agent(RandomWalker, start_position)
