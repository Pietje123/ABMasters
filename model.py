from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
import os
import numpy as np
from agents import *


class Classroom(Model):
	def __init__(self, floorplan):
		super().__init__()
		self.n_agents = 0
		self.agents = []
		self.schedules = ['Human']
		self.schedule_Human = SimultaneousActivation(self)
		self.exits = []
		with open('floorplans/' + floorplan) as f:
			self.floorplan = np.matrix([line.strip().split() for line in f.readlines()])

		size = self.floorplan.shape

		self.grid = MultiGrid(size[0], size[1], torus=False)


		for i in range(size[0]):
			for j in range(size[1]):
				value = str(self.floorplan[i,j])
				self.floorplan[i,j] = False
				if value == 'W':
					self.new_agent(Wall, (i,j))
					self.floorplan[i,j] = True

				elif value == 'F':
					self.floorplan[i,j] = True
					self.new_agent(Furniture, (i,j))
					self.new_agent(Human, (i,j))

				elif value == 'E':
					self.exits.append((i,j)) 
					self.new_agent(Exit, (i,j))

	def new_agent(self, agent_type, pos):
		'''
		Method that creates a new agent, and adds it to the correct scheduler.
		'''
		agent = agent_type(self, pos)
		self.grid.place_agent(agent, pos)
		if agent_type.__name__ in self.schedules:
			getattr(self, f'schedule_{agent_type.__name__}').add(agent)

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

tester = Classroom('floorplan_c0_110.txt')
tester.run_model()
# # Create a RandomWalker, so that we can call the random_move() method
# start_position = (5, 5)
# tester.new_agent(RandomWalker, start_position)