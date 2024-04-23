import numpy as np

RATE = 48000.
pad = 2**17
order = 3
geser = 150

def estimate_frequency(data):
    print("fft")
    #Windowing
    data *= np.hamming(len(data))
    #ZeroPadding
    data = np.pad(data,(0,pad-len(data)),'constant', constant_values=(0,0))
    #FFT
    fft = np.fft.rfft(data)
    fft = np.abs(fft)   # Calculate the magnitude spectrum of the signal
    #Harmonic Product Spectrum
    hps = []
    for i in range (1, order):
        hps.append(fft[::i+1])
    for j in range(len(hps)):
        for k in range(len(hps[j])):
            fft[k] *= hps[j][k]
    #Get the index of the maximum magnitude
    index = np.argmax(fft[geser:1000]) + geser
    #Filtering
    if geser < index:
        frequency = index * RATE / pad   # Calculate the frequency of the maximum magnitude
        return frequency
    else:
        return index
    
    #peaks,_ = find_peaks(fft, height = 0.1)
    #for i in peaks:
    #    print(i*RATE/pad)
    #if len(peaks) == 0:
    #    return 0
    #return peaks[0]*RATE/pad

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
            frek = estimate_frequency(x)
            print(frek)
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("Program Berhenti")
            break
