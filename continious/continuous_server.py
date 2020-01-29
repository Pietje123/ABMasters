from os import listdir, path
from collections import defaultdict

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter

from continuous_model import Classroom
from continuous_agents import Exit, Wall, Furniture, Human

class ContinuousCanvasGrid(VisualizationElement):

    package_includes = ["GridDraw.js", "CanvasModule.js", "InteractionHandler.js"]

    def __init__(self, portrayal_method, grid_width, grid_height,
                 canvas_width=500, canvas_height=500):
        super().__init__()

        self.portrayal_method = portrayal_method
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        new_element = ("new CanvasModule({}, {}, {}, {})"
            .format(self.canvas_width, self.canvas_height,
                self.grid_width, self.grid_height))

        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        grid_state = defaultdict(list)
        objects = model.humans + model.exits
        for obj in objects:
            portrayal = self.portrayal_method(obj)
            if portrayal:
                grid_state[portrayal["Layer"]].append(portrayal)

        return grid_state

# Creates a visual portrayal of our model in the browser interface
def fire_evacuation_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    (x, y) = agent.get_position()
    print(x, y)
    portrayal["x"] = x
    portrayal["y"] = y

    if type(agent) is Human:
        portrayal["scale"] = 1
        portrayal["Layer"] = 5

        # Normal agent
        portrayal["Shape"] = "resources/human.png"

    elif type(agent) is Exit:
        portrayal["Shape"] = "resources/fire_exit.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1

    elif type(agent) is Wall:
        portrayal["Shape"] = "resources/wall.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1

    elif type(agent) is Furniture:
        portrayal["Shape"] = "resources/furniture.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1

    return portrayal


# Size of grid is hardcoded, if floorplan changes change grid size manually
canvas_element = ContinuousCanvasGrid(fire_evacuation_portrayal, 23, 17)

# Define the charts on our web interface visualisation
status_chart = ChartModule([{"Label": "Escaped", "Color": "green"}])

# Get list of available floorplans

floor_plans = [f for f in listdir("floorplans")]

# Specify the parameters changeable by the user, in the web interface
model_params = {
    "floorplan": UserSettableParameter("choice", "Floorplan", value=floor_plans[0], choices=floor_plans),
    "human_count": UserSettableParameter("number", "Number Of Human Agents", value=1),
    #"random_spawn": UserSettableParameter('checkbox', 'Spawn Agents at Random Locations', value=True),
    #"save_plots": UserSettableParameter('checkbox', 'Save plots to file', value=True)
}

# Start the visual server with the model
server = ModularServer(Classroom, [canvas_element], "Fire Evacuation",
                      model_params)

# """With status chart"""
# server = ModularServer(Classroom, [canvas_element, status_chart], "Fire Evacuation", model_params)
