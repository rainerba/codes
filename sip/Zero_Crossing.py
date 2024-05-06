import numpy as np
import matplotlib.pyplot as plt

# def main(x):
#     zero_crossings = np.where(np.diff(np.sign(x)))[0]
#     time_between_crossings = np.diff(zero_crossings)
#     avg_time_between_crossings = np.mean(time_between_crossings)
#     freq = 48000. / avg_time_between_crossings / 2.
#     return freq


def main(x):
    plt.plot(x, label = 'asli')
    # Duplikasi data
    #x = np.append(x,x) # 16_384
    #x = np.append(x,x) # 32_768
    #x = np.append(x,x) # 65_536
    
    # Simple Moving Average
    x = np.convolve(x,np.ones(128), 'same')
    plt.plot(x, label = 'SMA')

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
