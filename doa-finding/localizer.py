#!/usr/bin/env python3

import math
import sys

import matplotlib
import matplotlib.pyplot as plt
import pyroomacoustics as pra
import numpy as np
import scipy.io.wavfile

fs, raw_data = scipy.io.wavfile.read(sys.argv[1])
print(f"Detected sampling frequency: {fs}Hz")
print(f"Found {raw_data.shape[1]} channels.")
raw_channels = raw_data.T
channels = np.copy(raw_channels)
# channels[1] = raw_channels[2]
# channels[2] = raw_channels[1]
# channels = raw_data.T[::-1]

c = 13503.94    # speed of sound in inches/second
nfft = 256  # FFT size
freq_range = [300, 3500]

mic_positions = pra.circular_2D_array(center=(0, 0), M=3, phi0=-math.pi / 6, radius=8.66)
print(mic_positions)

X = np.array([pra.stft(channel, nfft, nfft // 2, transform=np.fft.rfft).T for channel in channels])

doa = pra.doa.algorithms["MUSIC"](mic_positions, fs, nfft, c=c, num_src=1, max_four=4)
doa.locate_sources(X, freq_range=freq_range)
# IPython.embed()

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

if len(sys.argv) > 2:
    plt.savefig(sys.argv[2])
    print(f"Saved to {sys.argv[2]}")
else:
    plt.show()
