import numpy as np
import matplotlib.pyplot as plt

RATE = 48000.
pad = 2**17
order = 3
batas = [200,1000]

def main(data):
    # Windowing
    data *= np.hamming(len(data))
    # ZeroPadding
    data = np.pad(data,(0,pad-len(data)),'constant', constant_values=(0,0))
    # FFT
    fft = np.fft.rfft(data)
    fft = np.abs(fft)   # Calculate the magnitude spectrum of the signal
    # Harmonic Product Spectrum
    hps = []
    for i in range (1, order):
        hps.append(fft[::i+1])
    for j in range(len(hps)):
        for k in range(len(hps[j])):
            fft[k] *= hps[j][k]
    # Get the index of the maximum magnitude
    index = np.argmax(fft[batas[0]:batas[1]]) + batas[0]
    # Filtering
    if batas[0] < index:
        frequency = index * RATE / pad   # Calculate the frequency of the maximum magnitude
        return frequency
    else:
        return index

if __name__ == '__main__':
    import audio
    while True:
        try:
            x = audio.ambil_data()
            frek = main(x)
            print(frek)
        except KeyboardInterrupt:
            audio.stop()
            break