import os

import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector
from mesa import Model
from mesa.space import ContinuousSpace

from continuous_scheduler import DistanceScheduler
import continuous_agents as ca

class Classroom(Model):
	def __init__(self, floorplan, human_count):
		super().__init__()
		self.n_agents = human_count
		self.floorplan = []
		self.humans = []
		self.obstacles = []
		self.exits = []
		self.spawns = []
		self.scheduler = DistanceScheduler(self)

		# Loads floorplan textfile
		with open('C:/Users/jozse/github/ABMasters/floorplans/' + floorplan) as f:
			[self.floorplan.append(line.strip().split()) for line in f.readlines()]

		# Creates continuous Mesa space & discrete grid for pathfinding
		size = len(self.floorplan[0]) , len(self.floorplan)
		self.space = ContinuousSpace(size[0], size[1], torus=False)
		self.grid = []

		for y in range(6 * size[1]):
			row = []
			for x in range(6 * size[0]):
				row.append(ca.Node((x, y)))
			self.grid.append(row)

        # Places all elements in Mesa space and grid
		for x in range(size[0]):
			for y in range(size[1]):
				value = str(self.floorplan[y][x])

				if value == 'W':
					self.new_agent(ca.Wall, (x, y))
					for i in range(6 * x, 6 * (x + 1)):
						for j in range(6 * y, 6 * (y + 1)):
							self.grid[j][i].done = True

				elif value == 'F':
					self.new_agent(ca.Furniture, (x, y))
					for i in range(6 * x, 6 * (x + 1)):
						for j in range(6 * y, 6 * (y + 1)):
							self.grid[j][i].done = True

				elif value == 'S':
					self.spawns.append((x, y))

				elif value == 'E':
					self.new_agent(ca.Exit, (x, y))
					i = 6 * x + 1
					j = 6 * y + 1
					self.grid[j][i].exit = True

		# Spawn specified number of Humans in spawn points
		humans = rnd.sample(self.spawns, self.n_agents)
		for pos in humans:
			self.new_agent(ca.Human, pos)
		print("Classroom initialised.")

	def new_agent(self, agent_type, pos):
		'''
		Method that creates a new agent, and adds it to the correct list.
		'''
		agent = agent_type(self, pos)
		self.space.place_agent(agent, pos)

		if agent_type.__name__ == "Human":
			self.humans.append(agent)
		elif agent_type.__name__ == "Exit":
			self.exits.append(agent)
		else:
			self.obstacles.append(agent)

	def remove_agent(self, agent):
		'''
		Method that removes an agent from the grid and the correct scheduler.
		'''
		self.space.remove_agent(agent)
		if {type(agent).__name__} == "Human":
			self.scheduler.remove(agent)
			self.humans.remove(agent)

	def step(self):
		'''
		Method that steps every agent.
		'''
		self.scheduler.step()

	def run_model(self):
		self.step()

from mesa import Model
from mesa.space import ContinuousSpace
import os
import numpy as np
import random as rnd
import continuous_agents as ca
from mesa.datacollection import DataCollector
from continuous_scheduler import DistanceScheduler

import matplotlib.pyplot as plt

class Classroom(Model):
	def __init__(self, floorplan, human_count):
		super().__init__()
		self.n_agents = human_count
		self.floorplan = []
		self.humans = []
		self.obstacles = []
		self.exits = []
		self.spawns = []
		self.scheduler = DistanceScheduler(self)

		# Creates continuous Mesa space & discrete grid for pathfinding
		size = len(self.floorplan[0]) , len(self.floorplan)
		self.space = ContinuousSpace(size[0], size[1], torus=False)
		self.grid = []

		for y in range(6 * size[1]):
			row = []
			for x in range(6 * size[0]):
				row.append(ca.Node((x, y)))
			self.grid.append(row)

        # Places all elements in Mesa space and grid
		for x in range(size[0]):
			for y in range(size[1]):
				value = str(self.floorplan[y][x])

				if value == 'W':
					self.new_agent(ca.Wall, (x, y))
					for i in range(6 * x, 6 * (x + 1)):
						for j in range(6 * y, 6 * (y + 1)):
							self.grid[j][i].done = True

				elif value == 'F':
					self.new_agent(ca.Furniture, (x, y))
					for i in range(6 * x, 6 * (x + 1)):
						for j in range(6 * y, 6 * (y + 1)):
							self.grid[j][i].done = True

				elif value == 'S':
					self.spawns.append((x, y))

				elif value == 'E':
					self.new_agent(ca.Exit, (x, y))
					i = 6 * x + 1
					j = 6 * y + 1
					self.grid[j][i].exit = True

		# Spawn n_agents according to floorplan
		for pos in rnd.sample(self.spawns, self.n_agents):
			self.new_agent(ca.Human, pos)


	def new_agent(self, agent_type, pos):
		'''
		Method that creates a new agent, and adds it to the correct list.
		'''
		agent = agent_type(self, pos)
		self.space.place_agent(agent, pos)

		if agent_type.__name__ == "Human":
			self.humans.append(agent)
		elif agent_type.__name__ == "Exit":
			self.exits.append(agent)
		else:
			self.obstacles.append(agent)

	def remove_agent(self, agent):
		'''
		Method that removes an agent from the grid and the correct scheduler.
		'''
		self.space.remove_agent(agent)
		if {type(agent).__name__} == "Human":
			self.scheduler.remove(agent)
			self.humans.remove(agent)

	def step(self):
		'''
		Method that steps every agent.
		'''
		self.scheduler.step()

	def run_model(self):
		self.step()
