#!/usr/bin/env python3

import sys

import matplotlib
import matplotlib.pyplot as plt
import pyroomacoustics as pra
import numpy as np
import scipy.io.wavfile

fs, raw_data = scipy.io.wavfile.read(sys.argv[1])
print(f"Detected sampling frequency: {fs}Hz")
channels = raw_data.T

c = 343.    # speed of sound
nfft = 256  # FFT size
freq_range = [300, 3500]

mic_positions = pra.circular_2D_array(center=(0, 0), M=2, phi0=0, radius=(1 / 2))

X = np.array([pra.stft(channel, nfft, nfft // 2, transform=np.fft.rfft).T for channel in channels])

doa = pra.doa.algorithms["SRP"](mic_positions, fs, nfft, c=c, num_src=1, max_four=4)
doa.locate_sources(X, freq_range=freq_range)

spatial_resp = doa.grid.values
phi_plt = doa.grid.azimuth

base = 1.
height = 10.
true_col = [0, 0, 0]

fig = plt.figure()
ax = fig.add_subplot(111, projection="polar")
c_phi_plt = np.r_[phi_plt, phi_plt[0]]
c_dirty_img = np.r_[spatial_resp, spatial_resp[0]]
ax.plot(c_phi_plt, base + height * c_dirty_img, linewidth=3,
        alpha=0.55, linestyle='-',
        label="spatial spectrum")
plt.show()
