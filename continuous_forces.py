import numpy as np

def dijkstraforce(pos, targ):
    xs, ys = pos
    xe, ye = targ
    dx, dy = (xe / 3 - xs), (ye / 3 - ys)
    try:
        theta = np.arctan(dy / dx)
    except ZeroDivisionError:
        if dy > 0:
            theta = np.pi / 2
        elif dy < 0:
            theta = -np.pi/2
    fx, fy = 0.1 * np.cos(theta), 0.1 * np.sin(theta)

    return fx, fy

def bodyforce(pos, humans):
    fx, fy = 0, 0
    print(humans)
    for human in humans:
        if human.pos != pos:
                xs, ys = pos
                xe, ye = human.pos
                print(xs, ys, xe, ye)
                dx, dy = (xe - xs), (ye - ys)
                dist = np.sqrt((dx)**2 + (dy)**2)

                if dist < 1:
                    theta = np.arctan(dy / dx)
                    fx += -0.2 / dist * np.cos(theta)
                    fy += -0.5 / dist * np.sin(theta)
                    print(fx, fy)

    return (fx, fy)

def totalforce(pos, target, humans):

    dijkstra_x, dijkstra_y = dijkstraforce(pos, target)
    body_x, body_y = bodyforce(pos, humans)
    total_x, total_y = dijkstra_x + body_x, dijkstra_y + body_y

    return pos[0] + total_x, pos[1] + total_y
