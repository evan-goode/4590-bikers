To run either the doa-finding or the peak detection algorithm, first install the requisite dependencies:

pip3 install --user sympy matplotlib scipy pyaudio numpy pyroomacoustics

Then execute localizer.py, passing the path to a 3-channel WAV file as the first argument:

./doa-finding/localizer.py doa-finding/triangle-claps-1/2.wav
./peak-detection/localizer.py peak-detection/final_test/-18_18.wav

The live version of the peak-detection algorithm requires a 3+ channel audio interface. To use it, execute ./peak-detection/localizer.py with no arguments.
