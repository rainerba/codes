import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfilt

def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos')
    return sos

def butter_bandpass_filter(data, lowcut=75., highcut=350., fs=48000., order=6):
    sos = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sosfilt(sos, data)
    return y

# def main(x, senar):
    # batas = [[293.66,369.99],[220.0,277.18],[174.61,220.],[130.81,164.81],[98.,123.47],[73.42,92.5]]
    # x = butter_bandpass_filter(x, lowcut=batas[senar][0], highcut=batas[senar][1])

    # # Duplikasi data
    # #x = np.append(x,x) # 16_384
    # #x = np.append(x,x) # 32_768
    # #x = np.append(x,x) # 65_536
    
    # # Simple Moving Average
    # x = np.convolve(x,np.ones(20), 'same')
    # abs = np.abs(x)
    # max = np.max(abs)

    # zcrP = 0
    # zcrN = 0
    # N = len(x)
    # L = 1.2 * np.sum(abs) / N
    # xP = x-L
    # xN = x+L
    # if max > 0.:
        # for n in range(N-1):
            # if xP[n] < 0 < xP[n+1]:
                # zcrP+=1
            # if xN[n] < 0 < xN[n+1]:
                # zcrN+=1
        # freq = (48000. * (zcrP + zcrN) / N) / 2.
    # else:
        # freq = 0.
    # return freq, max
    
def main(x, senar):
    max = np.max(np.abs(x))
    batas = [[293.66,369.99],[220.0,277.18],[174.61,220.],[130.81,164.81],[98.,123.47],[73.42,92.5]]
    x = butter_bandpass_filter(x, lowcut=batas[senar][0], highcut=batas[senar][1])
    
    zeroC = np.where(np.diff(np.sign(x)))[0]
    time = np.diff(zeroC)
    avg = np.mean(time)
    if max > 0.01:
        freq = 48000. / avg / 2.
    else:
        freq = 0.
    return freq, max

if __name__ == '__main__':
    import audio
    import wave
    import pyaudio
    maxx = []
    frames = []
    senar = int(input("Pilih senar yang akan diatur: ")) - 1
    while True:
        try:
            x = audio.ambil_data()
            frames.append(x)
            frek,max = main(x,senar)
            print(frek)
            maxx.append(max)
        except KeyboardInterrupt:
            plt.plot(maxx)
            plt.show()
            audio.stop()
            wf = wave.open("zeroC.wav", 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paFloat32))
            wf.setframerate(48000)
            wf.writeframes(b''.join(frames))
            wf.close()
            print("Program berhenti")
            break
