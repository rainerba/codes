import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut=75., highcut=350., fs=48000., order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def main(x):
    # plt.plot(x, label = 'asli')
    x = butter_bandpass_filter(x)
    plt.plot(x, label = 'filtered')

    # Duplikasi data
    #x = np.append(x,x) # 16_384
    #x = np.append(x,x) # 32_768
    #x = np.append(x,x) # 65_536
    
    # Simple Moving Average
    # x = np.convolve(x,np.ones(64), 'same')
    # plt.plot(x, label = 'filtered')

    zcrP = 0
    zcrN = 0
    N = len(x)
    L = 1.2 * np.sum(np.abs(x)) / N
    xP = x-L
    xN = x+L
    for n in range(N-1):
        if xP[n] < 0 < xP[n+1]:
            zcrP+=1
        if xN[n] < 0 < xN[n+1]:
            zcrN+=1
    freq = (48000. * (zcrP + zcrN) / N) / 2.
    print(freq)
    plt.legend()
    plt.show()
    return freq

if __name__ == '__main__':
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
                input_device_index = 2)
    while True:
        try:
            y = stream.read(CHUNK, exception_on_overflow = False)
            data = np.frombuffer(y, dtype=np.float32)
            x = data.copy()
            x -= np.mean(x)
            frek = main(x)
            print(frek)
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("Program Berhenti")
            break
