import numpy as np
from scipy.signal import butter, sosfilt

def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos')
    return sos

def butter_bandpass_filter(data, lowcut=75., highcut=350., fs=48000., order=3):
    sos = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sosfilt(sos, data)
    return y

def main(x, senar):
    batas = [[293.66,369.99],[220.0,277.18],[174.61,220.],[130.81,164.81],[98.,123.47],[146.83,185.]]# senar 6 pakai harmoni pertama
    x = butter_bandpass_filter(x, lowcut=batas[senar][0], highcut=batas[senar][1])

    abs = np.abs(x)
    max = np.max(abs)
    N = len(x)
    L = 1.2 * np.sum(abs) / N
    xP = x-L
    xN = x+L
    
    zeroCP = np.where(np.diff(np.sign(xP)))[0]
    timeP = np.diff(zeroCP)
    avgP = np.mean(timeP)
    
    zeroCN = np.where(np.diff(np.sign(xN)))[0]
    timeN = np.diff(zeroCN)
    avgN = np.mean(timeN)
    
    avg = (avgP + avgN) / 2
    
    if max > 0.001:
        freq = 48000. / avg / 2.
        if senar == (6 - 1):
            freq /= 2.
    else:
        freq = 0.
    return freq

if __name__ == '__main__':
    import audio
    batas = [[293.66,369.99],[220.0,277.18],[174.61,220.],[130.81,164.81],[98.,123.47],[73.42,92.5]]
    senar = int(input("Pilih senar yang akan diatur: ")) - 1
    while True:
        try:
            x = audio.ambil_data()
            frek= main(x,senar)
            x = butter_bandpass_filter(x, lowcut=batas[senar][0], highcut=batas[senar][1])
            print(frek)
        except KeyboardInterrupt:
            audio.stop()
            break