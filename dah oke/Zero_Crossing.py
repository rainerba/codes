import numpy as np
import pyaudio
from scipy import signal

RATE = 48000
CHUNK = 1024
# check = 1

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

hitung = []
while True:
    try:
        data = stream.read(CHUNK)
        y = np.frombuffer(data, dtype=np.float32) #diubah ke numpy agar bisa diproses menggunakan library numpy
        y = y.copy()
        #-----------------------------------------------------#
        # smoothening = 1
        # chunk_size = 16
        # t = 0
        # while t < CHUNK // chunk_size:
        #     x = y[0 : chunk_size]
        #     i = 1
        #     MA = []
        #     MA.append(x[0])
        #     while i < len(x):
        #         window_average = (smoothening*x[i])+(1-smoothening)*MA[-1]
        #         MA.append(window_average)
        #         i += 1
        #     y[16 * t : 16 * (t + 1)] = MA
        #     t += 1
        #-------------------------------------------------#
        # chunk_size = 16
        # t = 0
        # window_size = 8
        # fixed = []
        # while t < CHUNK // chunk_size:
        #     x = temp[0 : chunk_size]
        #     i = 0
        #     MA = []
        #     while i < len(x) - window_size + 1:
        #         window_average = np.sum(x[i:i+window_size]) / window_size
        #         MA.append(window_average)
        #         i += 1
        #     fixed.append(MA)
        #     t += 1
        #-------------------------------------------------#
        
        sos = signal.butter(4,400,fs=RATE,output = 'sos')
        y = signal.sosfilt(sos,y)

        zero_crossings = np.where(np.diff(np.sign(y)))[0]
        if len(zero_crossings) > 0:
            # time_between_crossings = zero_crossings[1:] - zero_crossings[:-1]
            time_between_crossings = np.diff(zero_crossings)
            avg_time_between_crossings = np.mean(time_between_crossings)
            freq = RATE / avg_time_between_crossings / 2 #bagi 2 karena 1 crossing adalah setengah wave
            hitung.append(freq)
            if(len(hitung) == 10):
                freq = np.mean(hitung)
                print("%.2f Hz Zero-Crossing" %freq)
                hitung.clear()
            # print("check = %.f"%check)
            # check += 1
    except KeyboardInterrupt:
        print('Stopped by user')
        break
        