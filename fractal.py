import numpy as np
import matplotlib.pyplot as plt
import itertools, sys
import matplotlib as mpl

mpl.use('Cairo')

width=200
corner=width/2

fig = plt.figure(figsize=(20, 20))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-corner, corner), ax.set_xticks([])
ax.set_ylim(-corner, corner), ax.set_yticks([])

x_now = 0
y_now = 0

x=[]
y=[]

# expects a file containing a string of ACGT...
with open(sys.argv[1], "r") as fh:
    seq = fh.readline().strip()
    size = len(seq)
    count = 0
    for bp in seq[:10000000]:
        if bp == "A":
            x_now += (corner-x_now)/2
            y_now += (corner-y_now)/2
        elif bp == "T":
            x_now += (-corner-x_now)/2
            y_now += (corner-y_now)/2
        elif bp == "C":
            x_now += (corner-x_now)/2
            y_now += (-corner-y_now)/2
        elif bp == "G":
            x_now += (-corner-x_now)/2
            y_now += (-corner-y_now)/2
        x.append(x_now)
        y.append(y_now)
        count += 1
        if (count % 100000) == 0:
            sys.stdout.write(".")
            sys.stdout.flush()

ax.plot([round(a,2) for a in x],
        [round(b,2) for b in y],
        'b,', # blue pixels
        alpha=0.2,
        antialiased=True)

plt.savefig('cairo.png')
