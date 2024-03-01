import pyaudio
import numpy as np
from scipy.fft import fft
from scipy import signal
import matplotlib.pyplot as plt
import psutil

RATE = 48000
CHUNK = 16384
FORMAT = pyaudio.paFloat32
CHANNELS = 1
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
#Hanning Window
# window = 0.5 * (1-np.cos(np.linspace(0,2*np.pi, CHUNK, False)))

def estimate_frequency():
    data = stream.read(CHUNK)
    numpy_array = np.frombuffer(data, dtype=np.float32)
    array_copy = numpy_array.copy()

    array_copy *= signal.windows.hann(CHUNK)

    yf = np.fft.fft(array_copy)
    magnitudes = np.abs(yf[0:CHUNK])   # Calculate the magnitude spectrum of the signal

    new_magnitudes = magnitudes

    #####HPS#####
    # for i in range (len(magnitudes)//2):
    #     new_magnitudes[i] *= magnitudes[i*2]
    # for i in range (len(magnitudes)//3):
    #     new_magnitudes[i] *= magnitudes[i*3]
    # for i in range (len(magnitudes)//4):
    #     new_magnitudes[i] *= magnitudes[i*4]
    # for i in range (len(magnitudes)//5):
    #     new_magnitudes[i] *= magnitudes[i*5]                        
    #####HPS#####

    index = np.argmax(new_magnitudes)   # Get the index of the maximum magnitude
    frequency = index * RATE / CHUNK    # Calculate the frequency of the maximum magnitude
    # print("Baca:", frequency)
    # plt.plot(new_magnitudes)
    # plt.ylabel("amplitude")
    # plt.show()
    return frequency

if __name__ == '__main__':
    print("Mulai")
    pitch_before = 0.
    pitch_now = 0.
    while True:
        try:
            # print(f"CPU: {os.()}%")
            pitch_now = estimate_frequency()
            if 70 < pitch_now < 8000:
                if np.abs(pitch_now - pitch_before) < 5:
                    print(pitch_now, "FFT")
                pitch_before = pitch_now
        except KeyboardInterrupt:
            print('Stopped by user')
            break