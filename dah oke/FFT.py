import pyaudio
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

RATE = 48000
CHUNK = 2048 * 16
p = pyaudio.PyAudio()

def estimate_frequency(data):
    data *= signal.windows.hann(CHUNK)
    yf = np.fft.rfft(data)
    magnitudes = np.abs(yf)   # Calculate the magnitude spectrum of the signal

    order = 2
    #####HPS#####
    for i in range (1, order):
        hps = magnitudes[::i+1]
        for j in range(len(hps)):
            magnitudes[j] *=  hps[j]
    #####HPS#####
    index = np.argmax(magnitudes)   # Get the index of the maximum magnitude
    frequency = index * RATE / CHUNK    # Calculate the frequency of the maximum magnitude
    return frequency

if __name__ == '__main__':
    stream = p.open(format=pyaudio.paFloat32,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)
    print("Mulai")
    pitch_before = 0.
    pitch_now = 0.
    while True:
        try:
            y = stream.read(CHUNK)
            data = np.frombuffer(y, dtype=np.float32)
            x = data.copy()
            pitch_now = estimate_frequency(x)
            if 50 < pitch_now < 500:
                if np.abs(pitch_now - pitch_before) < 5:
                    print(pitch_now, "FFT")
            pitch_before = pitch_now
        except KeyboardInterrupt:
            print('Stopped by user')
            break