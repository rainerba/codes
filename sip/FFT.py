import numpy as np

RATE = 48000.
pad = 2**17
order = 3
batas = [200,1000]

def estimate_frequency(data):
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
            frek = estimate_frequency(x)
            print(frek)
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("Program Berhenti")
            break
