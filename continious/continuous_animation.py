import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

from continuous_model import Classroom


room = Classroom('floorplan_c0_110.txt', 80)
Writer = anim.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Jozsef'), bitrate=1800)
frames = []
for i in range(500):
    print(i)
    positions = []
    for human in room.humans:
        positions.append(human.pos)
    room.step()
    frames.append(positions)

fig, ax = plt.subplots()
ln, = plt.plot([], [], 'ro')

exit_x = []
exit_y = []
for exit in room.exits:
    exit_x.append(exit.pos[0])
    exit_y.append(exit.pos[1])

obs_x = []
obs_y = []
for obs in room.obstacles:
    obs_x.append(obs.pos[0])
    obs_y.append(obs.pos[1])

plt.plot([exit_x], [exit_y], 'go')
plt.plot([obs_x], [obs_y], 'bo')

def init():
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 25)
    return ln,

def update(frame):
    xdata, ydata = [], []
    for pos in frame:
        try:
            xdata.append(pos[0])
            ydata.append(pos[1])
        except Exception:
            pass
    ln.set_data(xdata, ydata)
    return ln,

ani = anim.FuncAnimation(fig, update, frames, init_func=init, blit=True)
ani.save(f"animation80.mp4", writer=writer)
