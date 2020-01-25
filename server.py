from os import listdir, path

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import Classroom
from agents import Exit, Wall, Furniture, Human


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


# Was hoping floorplan could dictate the size of the grid, but seems the grid needs to be specified first, so the size is fixed to 50x50
canvas_element = CanvasGrid(fire_evacuation_portrayal, 23, 17, 800, 800)

# Define the charts on our web interface visualisation
status_chart = ChartModule([{"Label": "Alive", "Color": "blue"},
                            {"Label": "Escaped", "Color": "green"}])

mobility_chart = ChartModule([{"Label": "Normal", "Color": "green"}])

# Get list of available floorplans

floor_plans = [f for f in listdir("floorplans")]

# Specify the parameters changeable by the user, in the web interface
model_params = {
    "floorplan": UserSettableParameter("choice", "Floorplan", value=floor_plans[0], choices=floor_plans),
    "human_count": UserSettableParameter("number", "Number Of Human Agents", value=10),
    #"random_spawn": UserSettableParameter('checkbox', 'Spawn Agents at Random Locations', value=True),
    #"save_plots": UserSettableParameter('checkbox', 'Save plots to file', value=True)
}

# Start the visual server with the model
server = ModularServer(Classroom, [canvas_element, status_chart, mobility_chart], "Fire Evacuation",
                       model_params)
