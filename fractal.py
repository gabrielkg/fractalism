import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import itertools

width=500

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-width/2, width/2), ax.set_xticks([])
ax.set_ylim(-width/2, width/2), ax.set_yticks([])

x_now = 0
y_now = 0

x=[]
y=[]

with open("/data/work/share/AK58/FINAL/v1/AK58_chr1B_v5/AK58_chr1B_v5.fa", "r") as fh:
    lines = fh.readlines()
    lines = lines[1:50000]
    for line in lines:
        for bp in line:
            if bp == "A":
                x_now = (x_now + 1) % width
            elif bp == "T":
                x_now = (x_now - 1) % width
            elif bp == "C":
                y_now = (y_now + 1) % width
            elif bp == "G":
                y_now = (y_now - 1) % width
            x.append(x_now)
            y.append(y_now)

plt.scatter([a-(width/2) for a in x], [b-(width/2) for b in y], alpha=.01, s=3)

plt.show()
