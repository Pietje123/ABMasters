from mesa import Agent
import random

class Objects(Agent):
	def __init__(self, model, pos):
		super().__init__(model.next_id(), model)
		self.pos = pos


class Furniture(Objects):
	def __init__(self, model, pos):
		super().__init__(model, pos)

class Wall(Objects):
	def __init__(self, model, pos):
		super().__init__(model, pos)

class Exit(Objects):
	def __init__(self, model, pos):
		super().__init__(model, pos)

class Human(Objects):
	def __init__(self, model, pos):
		super().__init__(model, pos)
		getattr(model, f'schedule_{self.__class__.__name__}').add(self)
		self.new_pos = 0

	def move(self):
		neighbourhood = self.model.grid.get_neighborhood(self.pos,
													moore=False)
		self.new_pos = random.choice(neighbourhood)

	def step(self):
		self.move() 

	def advance(self):
		self.model.grid.move_agent(self, self.new_pos)