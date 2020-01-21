import matplotlib.pyplot as plt
import numpy as np

exit = (-50, -15)

class Agent:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.radius = 1
        self.path = [self.pos, exit]

class Object:
    def __init__(self, x, y, name):
        self.pos = (x, y)
        self.rad_x = 3
        self.rad_y = 30
        self.name = name

def line(start, end, x=0):
    (xs, ys) = start
    (xe, ye) = end
    delta = (xe - xs), (ye - ys)
    rc = delta[1] / delta[0]
    b = ys - (xs * rc)
    y = rc * x + b
    return {'y': y, 'rc': rc, 'b': b}

def tan_line(rc, start, x=0):
    (xs, ys) = start
    rc = -1 / rc
    b = ys - (xs * rc)
    y = rc * x + b
    return {'y': y, 'rc': rc, 'b': b}

def avoid(start, end, object):
    rc1, b1 = line(start, end)['rc'], line(start, end)['b']
    rc2, b2 = tan_line(rc1, object.pos)['rc'], tan_line(rc1, object.pos)['b']
    x = (b2 - b1) / (rc1 - rc2)
    x_min = x
    x_plus = x

    while True:
        y_min = tan_line(rc1, object.pos, x_min)['y']
        y_plus = tan_line(rc1, object.pos, x_plus)['y']

        if ((x_min < object.pos[0] - object.rad_x - agent.radius or x_min > object.pos[0] + object.rad_x + agent.radius) and
            (y_min < object.pos[1] - object.rad_y - agent.radius or y_min > object.pos[1] + object.rad_y + agent.radius)):
            return (x_min, y_min)
        elif ((x_plus < object.pos[0] - object.rad_x - agent.radius or x_plus > object.pos[0] + object.rad_x + agent.radius) and
            (y_plus < object.pos[1] - object.rad_y - agent.radius or y_plus > object.pos[1] + object.rad_y + agent.radius)):
            return (x_plus, y_plus)
        else:
            x_min -= 0.1
            x_plus += 0.1

agent = Agent(25.0, 25.0)
object_1 = Object(-25.0, 0.0, 1)
object_2 = Object(-10.0, -10.0, 2)
object_3 = Object(-40.0, -15.0, 3)
objects = [object_1, object_2, object_3]
restart = True

for i in range(4):
    restart = False
    for i in range(len(agent.path) - 1):
        start, end = agent.path[i], agent.path[i+1]
        for x in np.linspace(start[0], end[0]):
            for object in objects:
                y = line(start, end, x)['y']
                if ((x > object.pos[0] - object.rad_x - agent.radius and x < object.pos[0] + object.rad_x + agent.radius) and
                    (y > object.pos[1] - object.rad_y - agent.radius and y < object.pos[1] + object.rad_y + agent.radius)):
                        node = avoid(start, end, object)
                        agent.path.insert(i + 1, node)
                        restart = True
                        break
            if restart:
                break
        if restart:
            break



# Scatter Agent & Exit
for node in agent.path:
    plt.scatter(node[0], node[1], c='b')

# Plot contours object and fill
for object in objects:
    plt.plot([object.pos[0] - object.rad_x, object.pos[0] + object.rad_x],
             [object.pos[1] + object.rad_y, object.pos[1] + object.rad_y], c='r')

    plt.plot([object.pos[0] - object.rad_x, object.pos[0] + object.rad_x],
              [object.pos[1] - object.rad_y, object.pos[1] - object.rad_y], c='r')

    plt.fill_between([object.pos[0] - object.rad_x, object.pos[0] + object.rad_x],
             [object.pos[1] + object.rad_y, object.pos[1] + object.rad_y],
             [object.pos[1] - object.rad_y, object.pos[1] - object.rad_y],
             color='r')

# Plot calculated lines
plt.plot(np.linspace(-50, 25), line(agent.pos, exit, np.linspace(-50, 25))['y'])

# Plot path
print(agent.path)
for i in range(len(agent.path) - 1):
    start = agent.path[i]
    end = agent.path[i+1]
    plt.plot(np.linspace(end[0], start[0]), line(start, end, np.linspace(end[0], start[0]))['y'], c='g')

plt.ylim(-50, 50)
plt.xlim(-50, 50)
plt.show()
