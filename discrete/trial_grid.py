from mesa.space import Grid

class trial_grid(Grid):
	def __init__(self, width, height, torus):
		super().__init__(width, height, torus)


	def get_free_cells(self, pos, moore=False):
		neighborhood = self.get_neighborhood(pos, moore)
		return[cell for cell in neighborhood if self.is_cell_empty(cell)]
