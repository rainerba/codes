import pyaudio
import numpy as np
from scipy.fft import fft
from scipy import signal
import matplotlib.pyplot as plt

RATE = 48000
CHUNK = 4096
FORMAT = pyaudio.paFloat32
CHANNELS = 1
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)


def estimate_frequency():
    data = stream.read(CHUNK)
    numpy_array = np.frombuffer(data, dtype=np.float32)

    yf = fft(numpy_array)
    magnitudes = np.abs(yf[0:CHUNK])   # Calculate the magnitude spectrum of the signal

    new_magnitudes = magnitudes

    #####HPS#####
    for i in range (len(magnitudes)//2):
        new_magnitudes[i] *= np.mean(magnitudes[i*2 : i*2+2])
    # for i in range (len(magnitudes)//3):
    #     new_magnitudes[i] *= np.mean(magnitudes[i*3 : i*3+3])
    # for i in range (len(magnitudes)//4):
    #     new_magnitudes[i] *= np.mean(magnitudes[i*4 : i*4+4])
    # for i in range (len(magnitudes)//5):
    #     new_magnitudes[i] *= np.mean(magnitudes[i*5 : i*5+5])                        
    #####HPS#####

    index = np.argmax(new_magnitudes)   # Get the index of the maximum magnitude
    frequency = index * RATE / CHUNK    # Calculate the frequency of the maximum magnitude
    return frequency

if __name__ == '__main__':
    print("Mulai")
    pitch_before = 0.
    pitch_now = 0.
    while True:
        try:
            pitch_now = estimate_frequency()
            if 50 < pitch_now < 8000:
                if np.abs(pitch_now - pitch_before) < 5:
                    print(pitch_now, "FFT")
                pitch_before = pitch_now
        except KeyboardInterrupt:
            print('Stopped by user')
            break