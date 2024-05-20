import numpy as np

metode = "zeroC"
f=329.63 # Frekuensi sinyal
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
    data -= np.mean(data)

    if metode == "yin":
        import Yin
        frek = Yin.main(data)
    elif metode == "fft":
        import FFT
        frek = FFT.main(data)
    elif metode == "zeroC":
        import Zero_Crossing
        frek = Zero_Crossing.main(data,senar=0)
    print(frek)
