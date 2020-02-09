from os import listdir, path

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from discrete.model import Classroom
from discrete.agents import Exit, Wall, Furniture, Human


# Creates a visual portrayal of our model in the browser interface
def fire_evacuation_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    (x, y) = agent.get_position()
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
canvas_element = CanvasGrid(fire_evacuation_portrayal, 23, 17, 500, 500)

# Define the charts on our web interface visualisation
status_chart = ChartModule([{"Label": "Escaped", "Color": "green"}])

# Get list of available floorplans

floor_plans = [f for f in listdir("floorplans")]

# Specify the parameters changeable by the user, in the web interface
model_params = {
    "floorplan": UserSettableParameter("choice", "Floorplan", value=floor_plans[0], choices=floor_plans),
    "human_count": UserSettableParameter("slider", "Number Of Human Agents", 10, 1, 80),
    "human_panic": UserSettableParameter("slider", "Panic", 0, 0, 7),
    "human_speed": UserSettableParameter("slider", "Maximum speed", 3, 1, 5),
}

"""With status chart"""
server = ModularServer(Classroom, [canvas_element, status_chart], "Fire Evacuation", model_params)
