import numpy as np
import matplotlib.pyplot as plt

metode = "zeroC"
f=330 # Frekuensi sinyal
t=1 # Lama sinyal dalam detik
harmonics = 6
fs = 48000.

if __name__ == '__main__':
    x = np.arange(t * fs) / fs
    signal = np.sin(2 * np.pi * f * x)
    # Harmoni
    for i in range(2,harmonics+1):
        signal += np.sin(2 * np.pi * f * i * x)/i
    # Amplitude berkurang
    envelope = lambda x: np.exp(-x)
    signal *= envelope(x)
    # Dengan noise
    # noise = np.random.normal(0, np.std(signal), len(signal))
    # signal += noise
    plt.plot(signal)
    plt.show()
    data = np.float32(signal)

    if metode == "yin":
        import Yin
        frek = Yin.process_audio(data)
    elif metode == "fft":
        import FFT
        frek = FFT.estimate_frequency(data)
    elif metode == "zeroC":
        import Zero_Crossing
        frek = Zero_Crossing.main(data)
    print(frek)