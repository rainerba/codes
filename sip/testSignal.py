import numpy as np
import matplotlib.pyplot as plt

metode = "zeroC"
f=330
t=1

harmonics = 6
fs = 48000.

if __name__ == '__main__':
    samples = np.arange(t * fs) / fs
    signal = np.sin(2 * np.pi * f * samples)
    for i in range(2,harmonics+1):
        signal += np.sin(2 * np.pi * f * i * samples)/i
    noise = np.random.normal(0, np.std(signal), len(signal))
    x = np.float32(signal)
    if metode == "yin":
        import Yin
        frek = Yin.process_audio(x)
    elif metode == "fft":
        import FFT
        frek = FFT.estimate_frequency(x)
    elif metode == "zeroC":
        import Zero_Crossing
        frek = Zero_Crossing.main(x)
    print(frek)