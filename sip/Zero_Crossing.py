import numpy as np
CHUNK = 2048
RATE = 48000

def main(x):
    zero_crossings = np.where(np.diff(np.sign(x)))[0]
    time_between_crossings = np.diff(zero_crossings)
    avg_time_between_crossings = np.mean(time_between_crossings)
    freq = 48000. / avg_time_between_crossings / 2.
    print(freq)
    return freq

if __name__ == '__main__':
    import pyaudio
    CHUNK = 2048
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