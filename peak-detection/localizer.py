#!/usr/bin/env python3

import os
import sys

from sympy import *
import sympy as sympy
import matplotlib.pyplot as plt
import scipy.io.wavfile
import pyaudio
import numpy as np

L = 11.5
ax = 0
ay = 6.43
bx = -L / 2
by = -3.439
cx = L / 2
cy = -3.439
k = 13503.9 # speed of sound in inches per second



def stream_mode():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 3
    RATE = 44100
    RECORD_SECONDS = 10
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    THRESHOLD = 26000
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        data_array = np.frombuffer(data, dtype='int16')
        channel0 = data_array[0::CHANNELS]
        channel1 = data_array[1::CHANNELS]
        channel2 = data_array[2::CHANNELS]
        if max(max(channel0), max(channel1), max(channel2)) > THRESHOLD:
            index0 = np.where(channel0 == max(channel0))[0][0]
            index1 = np.where(channel1 == max(channel1))[0][0]
            index2 = np.where(channel2 == max(channel2))[0][0]
            ta = (i+index0/CHUNK)*CHUNK/RATE
            tb = (i+index1/CHUNK)*CHUNK/RATE
            tc = (i+index2/CHUNK)*CHUNK/RATE
            break

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    return ta, tb, tc

def get_peak_time(raw_data, channel, fs, threshold):
    peak = 0
    t = -1
    for index, entry in enumerate(raw_data):
        time = index / fs #get time of sample in secs
        currValue = abs(entry[channel])
        if currValue > threshold:
            if peak == 0:
                peak = currValue
                t = time
            elif (peak < currValue):
                peak = currValue
                t = time
        elif peak > 0:
            break
    return t

def input_mode():
    fs, raw_data = scipy.io.wavfile.read(sys.argv[1])
    print(f"Detected sampling frequency: {fs}Hz")
    print(f"Found {raw_data.shape[1]} channels.")
    THRESHOLD = 0.75
    ta = get_peak_time(raw_data, 0, fs, THRESHOLD)
    tb = get_peak_time(raw_data, 1, fs, THRESHOLD)
    tc = get_peak_time(raw_data, 2, fs, THRESHOLD)
    return ta, tb, tc


def plotSrc(sol, c):
    plt.plot([sol[1]], [sol[2]], c+ 's')
    ax.add_artist(plt.Circle((sol[1], sol[2]), sol[0]+k*a_s, color=c, fill=False))
    ax.add_artist(plt.Circle((sol[1], sol[2]), sol[0]+k*b_s, color=c, fill=False))
    ax.add_artist(plt.Circle((sol[1], sol[2]), sol[0]+k*c_s, color=c, fill=False))

# (ax-x0)^2 + (ay-y0)^2 = r^2
# (bx-x0)^2 + (by-y0)^2 = (r+k*bs)^2
# (cx-x0)^2 + (cy-y0)^2 = (r+k*cs)^2
def solveAndPlot(a_s, b_s, c_s):
    L = 11.5
    ax = 0
    ay = 6.43
    bx = -L / 2
    by = -3.439
    cx = L / 2
    cy = -3.439
    k = 13503.9
    x = Symbol("x")
    y = Symbol("y")
    r = Symbol("r")
    solutions = solve([(ax-x)**2 + (ay-y)**2 - (r+k*a_s)**2, 
                   (bx-x)**2 + (by-y)**2 - (r+k*b_s)**2,
                   (cx-x)**2 + (cy-y)**2 - (r+k*c_s)**2], 
                    x, y, r, set=True)
    print(solutions)
    ax = plt.gca()
    errCount = 0
    for sol in solutions[1]:
        r = sol[0]
        x = sol[1]
        y = sol[2]
        # if (sol[0] > 0):
        try: 
            if (a_s == 0):
                if (r+k*a_s)**2 < (r+k*b_s)**2 and (r+k*a_s)**2 < (r+k*c_s)**2:
                    plotSrc(sol, 'b')
                else:
                    plotSrc(sol, 'g')
            elif (b_s == 0):
                if (r+k*b_s)**2 < (r+k*a_s)**2 and (r+k*b_s)**2 < (r+k*c_s)**2:
                    plotSrc(sol, 'b')
                else:
                    plotSrc(sol, 'g')
            elif (c_s == 0):
                if (r+k*c_s)**2 < (r+k*a_s)**2 and (r+k*c_s)**2 < (r+k*b_s)**2:
                    plotSrc(sol, 'b')
                else:
                    plotSrc(sol, 'g')
        except TypeError:
            errCount+=1
            if errCount > 1:
                print("System solution was imaginary - real solution could not be found :(")
                exit(0)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("Input Mode")
        ta, tb, tc = input_mode()
    else:
        print("Stream Mode")
        ta, tb, tc = stream_mode()

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

    print("times", ta, tb, tc)
    print("offsets", a_s, b_s, c_s)

    plt.plot([ax, bx, cx], [ay, by, cy], 'ro')
    plt.axis([-70, 70, -60, 60])
    ax = plt.gca()
    solveAndPlot(a_s, b_s, c_s)

    plt.show()
