import numpy as np

# def main(x):
#     zero_crossings = np.where(np.diff(np.sign(x)))[0]
#     time_between_crossings = np.diff(zero_crossings)
#     avg_time_between_crossings = np.mean(time_between_crossings)
#     freq = 48000. / avg_time_between_crossings / 2.
#     return freq

def main(x):
    hitungP = 0
    hitungN = 0
    N = len(x)
    L = 1.8 * np.sum(np.abs(x)) / N

    xP = x-L
    xN = x+L
    for n in range(N-1):
        if xP[n] < 0 < xP[n+1]:
            hitungP+=1
        if xN[n] < 0 < xN[n+1]:
            hitungN+=1
    zcrP = hitungP / N
    zcrN = hitungN / N
    freq = (48000. * (zcrP + zcrN)) / 2.
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
                frames_per_buffer=CHUNK)
    while True:
        try:
            y = stream.read(CHUNK, exception_on_overflow = False)
            data = np.frombuffer(y, dtype=np.float32)
            x = data.copy()
            frek = main(x)
            print(frek)
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("Program Berhenti")
            break
