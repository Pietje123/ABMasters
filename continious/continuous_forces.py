import numpy as np

def dijkstraforce(pos, targ):
    xs, ys = pos
    xe, ye = targ
    dx, dy = (xe / 3 - xs), (ye / 3 - ys)
    print(f"DF: {pos}, {targ}, {dx, dy}")
    if np.abs(dx) < 0.00001 or np.abs(dy) < 0.00001:
        if dx > 0.00001:
            theta = 0
        elif dx < -0.00001:
            theta = np.pi
        elif dy > 0.00001:
            theta = np.pi / 2
        elif dy < -0.00001:
            theta = -np.pi / 2
        else:
            return 0, 0
    else:
        if dx > 0 and dy > 0:
            theta = np.arctan(np.abs(dy / dx))
        elif dx < 0 and dy > 0:
            theta = np.pi - np.arctan(np.abs(dy / dx))
        elif dx > 0 and dy < 0:
            theta = -np.arctan(np.abs(dy / dx))
        elif dx < 0 and dy < 0:
            theta = np.pi + np.arctan(np.abs(dy / dx))

    fx, fy = 0.15 * np.cos(theta), 0.15 * np.sin(theta)
    print(f"Dijkstra fx: {fx}, fy: {fy}, theta: {theta}")
    return fx, fy

def bodyforce(pos, humans):
    fx, fy = 0, 0
    xs, ys = pos
    dist = 0

    for human in humans:
        try:
            if human.pos != pos:
                xe, ye = human.pos
                dx, dy = (xe - xs), (ye - ys)
                dist = np.sqrt((dx)**2 + (dy)**2)

                if dist < 0.5:
                    if np.abs(dx) < 0.00001 or np.abs(dy) < 0.00001:
                        if dx > 0.001:
                            theta = 0
                        elif dx < -0.00001:
                            theta = np.pi
                        elif dy > 0.00001:
                            theta = np.pi / 2
                        elif dy < -0.00001:
                            theta = -np.pi / 2
                    else:
                        if dx > 0 and dy > 0:
                            theta = np.arctan(dy / dx)
                        elif dx < 0 and dy > 0:
                            theta = np.pi - np.arctan(dy / dx)
                        elif dx > 0 and dy < 0:
                            theta = -np.arctan(dy / dx)
                        elif dx < 0 and dy < 0:
                            theta = np.pi + np.arctan(dy / dx)

                    fx += -0.07 / dist * np.cos(theta)
                    fy += -0.07 / dist * np.sin(theta)
        except TypeError:
            pass

    return (fx, fy)

def objectforce(pos, obstacles):
    fx, fy = 0, 0

    for obstacle in obstacles:
        xs, ys = pos
        xe, ye = obstacle.pos
        dx, dy = (xe - xs), (ye - ys)
        dist = np.sqrt((dx)**2 + (dy)**2)

    pass


def totalforce(pos, target, humans):

    dijkstra_x, dijkstra_y = dijkstraforce(pos, target)
    body_x, body_y = bodyforce(pos, humans)
    total_x, total_y = dijkstra_x + body_x, dijkstra_y + body_y

    return pos[0] + total_x, pos[1] + total_y
