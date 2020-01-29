from mesa import Model
from mesa.space import Grid
from mesa.time import SimultaneousActivation
import os
import numpy as np
from agents import *
from mesa.datacollection import DataCollector
from scheduler import DistanceScheduler

class Classroom(Model):
	def __init__(self, floorplan, human_count):
		super().__init__()
		self.n_agents = human_count
		self.agents = []
		self.schedules = ['Human']
		self.schedule_Human = DistanceScheduler(self)
		# SimultaneousActivation(self)
		self.exits = []
		self.floorplan = []
		self.spawn_list = []

		with open('floorplans/' + floorplan) as f:
			[self.floorplan.append(line.strip().split()) for line in f.readlines()]

		size = len(self.floorplan) , len(self.floorplan[0])
		self.grid = Grid(size[0], size[1], torus=False)

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
					self.spawn_list.append((i,j))

				elif value == 'E':
					self.floorplan[i][j].exit = True
					self.new_agent(Exit, (i,j))
					self.exits.append((i, j))

		# Spawn n_agents according to floorplan
		for pos in random.sample(self.spawn_list, self.n_agents):
			self.new_agent(Human, pos)


		# Collects statistics from our model run
		self.datacollector = DataCollector(
			{
				"Inside": lambda m: self.schedule_Human.get_agent_count(),
				"Escaped": lambda m: (self.n_agents - self.schedule_Human.get_agent_count())
			}
		)

		# for human in self.agents:
		# 	if type(human) is Human:
		# 		human.dijkstra()

	def new_agent(self, agent_type, pos):
		'''
		Method that creates a new agent, and adds it to the correct scheduler.
		'''
		agent = agent_type(self, pos)
		self.grid.place_agent(agent, pos)
		if agent_type.__name__ in self.schedules:
			# getattr(self, f'schedule_{agent_type.__name__}').add(agent)
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
		self.datacollector.collect(self)
		self.schedule_Human.step()

	def run_model(self):
		self.step()



		# tester = Classroom('floorplan_c0_110.txt', 80)
# for i in range(10):
# 	print("\n")
# 	print(i)
# 	for agent in tester.agents:
# 		print(agent.pos)
# 	tester.run_model()


#testagent = humans[0]
#print(testagent.pos)
#for i in range(5):
#	testagent.step()
#	print(testagent.pos)
