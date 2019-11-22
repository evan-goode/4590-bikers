#!/usr/bin/env python3

import sys
from sympy import *
import sympy as sympy
import matplotlib.pyplot as plt
import scipy.io.wavfile

L = 11.5
ax = 0
ay = 6.43
bx = -L / 2
by = -3.439
cx = L / 2
cy = -3.439
k = 13503.9 # speed of sound in inches per second

fs, raw_data = scipy.io.wavfile.read("./test/" + sys.argv[1] + ".wav")
print(f"Detected sampling frequency: {fs}Hz")
print(f"Found {raw_data.shape[1]} channels.")
# print(raw_data)

def show_info(aname, a):
    print ("Array", aname)
    print ("shape:", a.shape)
    print ("dtype:", a.dtype)
    print ("min, max:", a.min(), a.max())
    print()

# print(len(raw_data)/fs)
# show_info("raw", raw_data)

ta = -1
tb = -1
tc = -1

threshold = 0.6


def get_peak_time(raw_data, channel, fs, threshold):
    peak = 0
    t = -1
    for index, entry in enumerate(raw_data):
        time = index / fs #get time of sample in secs
        currValue = abs(entry[channel])
        # print("CurrValue", currValue)
        if currValue > threshold:
            # print(peak, currValue)
            if peak == 0:
                # print("get peak", time)
                peak = currValue
                t = time
            elif (peak < currValue):
                # print("new peak", time)
                peak = currValue
                t = time
        elif peak > 0:
            break
    return t

ta = get_peak_time(raw_data, 0, fs, threshold)
tb = get_peak_time(raw_data, 1, fs, threshold)
tc = get_peak_time(raw_data, 2, fs, threshold)


if ta < tb and ta < tc:
    a_s = 0
    b_s = tb - ta
    c_s = tc - ta
elif tb < ta and tb < tc:
    b_s = 0
    a_s = ta - tb
    c_s = tc - tb
elif tc < ta and tc < tb:
    c_s = 0
    a_s = ta - tc
    b_s = tb - tc

# rnd = 20
# a_s = round(a_s, rnd)
# b_s = round(b_s, rnd)
# c_s = round(c_s, rnd)

# a_s = 0
# b_s = 0
# c_s = 0

print("times", ta, tb, tc)

print("offsets", a_s, b_s, c_s)

x = Symbol("x")
y = Symbol("y")
r = Symbol("r")

# (ax-x0)^2 + (ay-y0)^2 = r^2
# (bx-x0)^2 + (by-y0)^2 = (r+k*bs)^2
# (cx-x0)^2 + (cy-y0)^2 = (r+k*cs)^2

solutions = solve([(ax-x)**2 + (ay-y)**2 - (r+k*a_s)**2, 
                   (bx-x)**2 + (by-y)**2 - (r+k*b_s)**2,
                   (cx-x)**2 + (cy-y)**2 - (r+k*c_s)**2], 
                    x, y, r, set=True)

print(solutions)
# for sol in solutions:
#     for entry in sol:
#         if type(entry) is not tuple:
#             print(type(entry))
#             continue
#         for n in entry: 
#             print(type(n), n)
# print(solutions)

plt.plot([ax, bx, cx], [ay, by, cy], 'ro')

plt.axis([-60, 60, -60, 60])
ax = plt.gca()

for sol in solutions[1]:
    # if (sol[0] > 0):
    plt.plot([sol[1]], [sol[2]], 'bs')
    ax.add_artist(plt.Circle((sol[1], sol[2]), sol[0]+k*a_s, color='b', fill=False))
    ax.add_artist(plt.Circle((sol[1], sol[2]), sol[0]+k*b_s, color='b', fill=False))
    ax.add_artist(plt.Circle((sol[1], sol[2]), sol[0]+k*c_s, color='b', fill=False))

plt.show()