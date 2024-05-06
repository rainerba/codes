import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut=75., highcut=350., fs=48000., order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def main(x, senar):
    batas = [[293.66,369.99],[220.0,277.18],[174.61,220.],[130.81,164.81],[98.,123.47],[73.42,92.5]]
    # plt.plot(x, label = 'asli')
    x = butter_bandpass_filter(x)
    # plt.plot(x, label = 'filtered')

    # Duplikasi data
    #x = np.append(x,x) # 16_384
    #x = np.append(x,x) # 32_768
    #x = np.append(x,x) # 65_536
    
    # Simple Moving Average
    x = np.convolve(x,np.ones(20), 'same')
    abs = np.abs(x)
    max = np.max(abs)
    # plt.plot(x, label = 'filtered')

    zcrP = 0
    zcrN = 0
    N = len(x)
    L = 1.2 * np.sum(abs) / N
    xP = x-L
    xN = x+L
    if max > 0.03:
        for n in range(N-1):
            if xP[n] < 0 < xP[n+1]:
                zcrP+=1
            if xN[n] < 0 < xN[n+1]:
                zcrN+=1
        freq = (48000. * (zcrP + zcrN) / N) / 2.
    else:
        freq = 0.
    # plt.legend()
    # plt.show()
    print(freq)
    return freq, max

if __name__ == '__main__':
    maxx = []
    import pyaudio
    CHUNK = 8192
    RATE = 48000
    p =  pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK,
                input_device_index = 1)
    while True:
        try:
            y = stream.read(CHUNK, exception_on_overflow = False)
            data = np.frombuffer(y, dtype=np.float32)
            x = data.copy()
            x -= np.mean(x)
            frek,max = main(x)
            maxx = np.append(maxx, max)
        except KeyboardInterrupt:
            plt.plot(maxx)
            plt.show()
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("Program Berhenti")
            break
