import numpy as np
import matplotlib.pyplot as plt
import itertools, sys
import matplotlib as mpl

def close_window(evt):
    exit()

width=200
corner=width/2

fig = plt.figure(figsize=(10, 10))

# make plot interactive for continuous drawing
plt.ion()

# connect close window event to handler function
fig.canvas.mpl_connect('close_event', close_window)

ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-corner, corner), ax.set_xticks([])
ax.set_ylim(-corner, corner), ax.set_yticks([])

x_now = 0
y_now = 0

x=[]
y=[]

# for experiments
factor=2

# expects a file containing a string of ACGT...
with open(sys.argv[1], "r") as fh:
    seq = fh.readline().strip()
    size = len(seq)
    count = 0
    for bp in seq[:5000000]:
        if bp in ["A", "C", "G", "T"]:
            if bp == "T": # top right
                x_now += (corner-x_now)/factor
                y_now += (corner-y_now)/factor
            elif bp == "A": # top left
                x_now += (-corner-x_now)/factor
                y_now += (corner-y_now)/factor
            elif bp == "C": # bottom right
                x_now += (corner-x_now)/factor
                y_now += (-corner-y_now)/factor
            elif bp == "G": # bottom left
                x_now += (-corner-x_now)/factor
                y_now += (-corner-y_now)/factor
            x.append(x_now)
            y.append(y_now)
            count += 1
            if (count % 10000) == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
                ax.plot(x,
                        y,
                        '.', # points
                        alpha=0.1,
                        markersize=2,
                        antialiased=True,
                        color='#003366')
                plt.show()
                plt.pause(0.0001)
                x = []
                y = []

