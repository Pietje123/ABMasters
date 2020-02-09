from mesa import Model
from discrete.trial_grid import *
from mesa.time import SimultaneousActivation
import os
import numpy as np
from discrete.agents import *
from mesa.datacollection import DataCollector
from discrete.scheduler import DistanceScheduler

class Classroom(Model):
	def __init__(self, human_count, human_weight=3, human_panic=0.0, human_speed=3, floorplan='0'):
		super().__init__()
		self.n_agents = human_count
		self.agents = []
		self.schedules = ['Human']
		self.schedule_Human = DistanceScheduler(self)
		self.schedule = self.schedule_Human
		self.exits = []
		self.floorplan = []
		self.spawn_list = []

		with open('floorplans/' + floorplan) as f:
			[self.floorplan.append(line.strip().split()) for line in f.readlines()]

		size = len(self.floorplan) , len(self.floorplan[0])
		self.grid = trial_grid(size[0], size[1], torus=False)

		for i in range(size[0]):
			for j in range(size[1]):
				value = str(self.floorplan[i][j])
				self.floorplan[i][j] = Node(i,j)
				if value == 'W':
					self.new_agent(Wall, (i,j), 1000)

				elif value == 'F':
					self.new_agent(Furniture, (i,j), 1000)

				elif value == 'S':
					self.spawn_list.append((i,j))

				elif value == 'E':
					self.floorplan[i][j].exit = True
					self.new_agent(Exit, (i,j), 0)
					self.exits.append((i, j))

		# Spawn n_agents according to floorplan
		for pos in random.sample(self.spawn_list, self.n_agents):
			self.new_agent(Human, pos, human_weight, human_panic, human_speed)


		# Collects statistics from our model run
		self.datacollector = DataCollector(
			{
				"Inside": lambda m: self.schedule_Human.get_agent_count(),
				"Escaped": lambda m: (self.n_agents - self.schedule_Human.get_agent_count())
			}
		)

	def new_agent(self, agent_type, pos, weight, human_panic= 0.0, human_speed = 3):
		'''
		Method that creates a new agent, and adds it to the correct scheduler.
		'''
		human_panic = human_panic / 10
		agent = agent_type(self, pos, weight, human_panic, human_speed) if agent_type == 'Human' else agent_type(self, pos, weight)
		self.grid.place_agent(agent, pos)
		if agent_type.__name__ in self.schedules:
			# getattr(self, f'schedule_{agent_type.__name__}').add(agent)
			self.agents.append(agent)

	def remove_agent(self, agent):
		'''
		Method that removes an agent from the grid and the correct scheduler.
		'''
		self.grid.remove_agent(agent)
		self.agents.remove(agent)
		getattr(self, f'schedule_{type(agent).__name__}').remove(agent)


	def step(self):
		'''
		Method that steps every agent.
		'''
		self.datacollector.collect(self)

		if not self.agents:
			self.running = False

		self.schedule_Human.step()

	def run_model(self):
		while self.agents:
			self.step()
