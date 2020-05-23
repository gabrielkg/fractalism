import numpy as np
import matplotlib.pyplot as plt
import itertools, sys
import matplotlib as mpl
import argparse

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

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str,
                    help="input file")
parser.add_argument("-s", "--start", type=int,
                    help="start position (bp)",
                    default=1)
parser.add_argument("-e", "--end", type=int,
                    help="end position (bp)",
                    default=1000000)
parser.add_argument("-a", "--alpha", type=float,
                    help="alpha value for points",
                    default=0.05)
parser.add_argument("--step", type=int,
                    help="sample every <step> (bp)",
                    default=1)
args = parser.parse_args()

# expects a file containing a string of ACGT...
with open(args.file, "r") as fh:
    seq = fh.readline().strip()
    size = len(seq)
    start, end = args.start, min(args.end, size)
    count = 0
    for bp in seq[args.start-1:end:args.step]:
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
                        alpha=args.alpha,
                        markersize=2,
                        antialiased=True,
                        color='#035efc')
                        #color='#003366')
                plt.show()
                plt.pause(0.0001)
                x = []
                y = []

