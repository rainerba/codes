import numpy as np

metode = "zeroC"
f=82.41 # Frekuensi sinyal
CHUNK = 8192
harmonics = 6
fs = 48000.

if __name__ == '__main__':
    x = np.arange(CHUNK) / fs
    signal = np.sin(2 * np.pi * f * x)
    # Harmoni
    for i in range(2,harmonics+1):
        signal += np.sin(2 * np.pi * f * i * x) / i
    # Amplitude berkurang
    envelope = lambda x: np.exp(-x)
    signal *= envelope(x)
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
