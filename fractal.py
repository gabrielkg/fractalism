import numpy as np
import matplotlib.pyplot as plt
import itertools, sys
import matplotlib as mpl
import argparse
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter

mpl.use("Qt5Agg")

def close_window(evt):
    exit()

width=200
corner=width/2

fig = plt.figure(figsize=(10, 10))

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
parser.add_argument("--animate",
                    help="generate animation",
                    action="store_true",
                    default=False)
parser.add_argument("--animateout", type=str,
                    help="output animation to file")
args = parser.parse_args()

print(mpl.get_backend())

def calculateNext(bp, x_now, y_now, corner, factor):
    x_next = x_now
    y_next = y_now
    if bp == "T": # top right
        x_next += (corner-x_now)/factor
        y_next += (corner-y_now)/factor
    elif bp == "A": # top left
        x_next += (-corner-x_now)/factor
        y_next += (corner-y_now)/factor
    elif bp == "C": # bottom right
        x_next += (corner-x_now)/factor
        y_next += (-corner-y_now)/factor
    elif bp == "G": # bottom left
        x_next += (-corner-x_now)/factor
        y_next += (-corner-y_now)/factor
    return x_next, y_next

# expects a file containing a string of ACGT...
with open(args.file, "r") as fh:
    seq = fh.readline().strip()
    size = len(seq)
    start, end = args.start, min(args.end, size)
    if args.animate:
        graph, = ax.plot([],
                         [],
                         '.',
                         markersize=2,
                         color='#035efc',
                         alpha=0.1)
        def animation(i):
            global x
            global y
            global x_now
            global y_now
            x_buff = []
            y_buff = []
            step = 2000
            for bp in seq[(i-1)*step:(i*step)-1]:
                if bp in ["A", "C", "G", "T"]:
                    x_now, y_now = calculateNext(bp,
                                                 x_now,
                                                 y_now,
                                                 corner,
                                                 factor)
                    x_buff.append(x_now)
                    y_buff.append(y_now)
            x += x_buff
            y += y_buff
            graph.set_data(x, y)
            return graph,
        ani = FuncAnimation(fig, animation, frames=500, interval=3)
        if args.animateout:
            FFwriter = FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
            ani.save('fractal.mp4', writer=FFwriter)
        else:
            plt.show()
    else:
        # plot single image
        for bp in seq[args.start-1:end:args.step]:
            if bp in ["A", "C", "G", "T"]:
                x_now, y_now = calculateNext(bp,
                                             x_now,
                                             y_now,
                                             corner,
                                             factor)
                x.append(x_now)
                y.append(y_now)
        ax.plot(x,
                y,
                '.', # points
                alpha=args.alpha,
                markersize=2,
                antialiased=True,
                color='#035efc')
                #color='#003366')
        plt.show()
