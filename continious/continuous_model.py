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

		with open('floorplans/' + floorplan) as f:
			[self.floorplan.append(line.strip().split()) for line in f.readlines()]

		size = len(self.floorplan[0]) , len(self.floorplan)
		self.space = ContinuousSpace(size[0], size[1], torus=False)
		self.grid = []

		for y in range(3 * size[1]):
			row = []
			for x in range(3 * size[0]):
				row.append(ca.Node((x, y)))
			self.grid.append(row)

		for x in range(size[0]):
			for y in range(size[1]):
				value = str(self.floorplan[y][x])

				if value == 'W':
					self.new_agent(ca.Wall, (x, y))
					for i in range(3 * x, 3 * (x + 1)):
						for j in range(3 * y, 3 * (y + 1)):
							self.grid[j][i].done = True

				elif value == 'F':
					self.new_agent(ca.Furniture, (x, y))
					for i in range(3 * x, 3 * (x + 1)):
						for j in range(3 * y, 3 * (y + 1)):
							self.grid[j][i].done = True

				elif value == 'S':
					self.spawns.append((x, y))

				elif value == 'E':
					self.new_agent(ca.Exit, (x, y))
					i = 3 * x + 1
					j = 3 * y + 1
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

# tester = Classroom('floorplan_c0_110.txt', 80)
# print(f"Exits: {tester.exits[0].pos, tester.exits[1].pos}")
#
#
# positions = []
# exits = []
#
# for row in tester.grid:
# 	for node in row:
# 		if node.done:
# 			positions.append(node.pos)
# 		if node.exit:
# 			exits.append(node.pos)
#
# xdata = []
# ydata = []
# xexit = []
# yexit = []
#
# for pos in positions:
# 	xdata.append(pos[0])
# 	ydata.append(pos[1])
#
# for pos in exits:
# 	xexit.append(pos[0])
# 	yexit.append(pos[1])
#
# plt.scatter(xdata, ydata)
# plt.scatter(xexit, yexit, c='g')
# plt.show()
#
# tester.run_model()
