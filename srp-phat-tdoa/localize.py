#!/usr/bin/env python3

import itertools
import sys

import matplotlib
import matplotlib.pyplot as plt
import pyroomacoustics as pra
import numpy as np
import scipy.io.wavfile

import IPython

fs, raw_data = scipy.io.wavfile.read(sys.argv[1])
print(f"Detected sampling frequency: {fs}Hz")
print(f"Found {raw_data.shape[1]} channels.")
channels = raw_data.T

c = 343.    # speed of sound
nfft = 256  # FFT size
freq_range = [300, 3500]

mic_positions = pra.circular_2D_array(center=(0, 0), M=3, phi0=0, radius=0.19685)

X = np.array([pra.stft(channel, nfft, nfft // 2, transform=np.fft.rfft).T for channel in channels])

pairs = itertools.combinations(range(X.shape[0]), r=2)

tdoa_func = lambda x, y: pra.experimental.localization.tdoa(x, y, interp=1, fs=fs)

tdoas = [tdoa_func(X.T[a], X.T[b]) for a, b in pairs]
print(tdoas)

IPython.embed()
