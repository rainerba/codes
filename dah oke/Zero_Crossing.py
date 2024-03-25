import numpy as np
# from scipy import signal

#CHUNK = 1024

hitung = []
def main(x):
    #-----------------------------------------------------#
    # smoothening = 1
    # chunk_size = 16
    # t = 0
    # while t < CHUNK // chunk_size:
    #     x = y[0 : chunk_size]
    #     i = 1
    #     MA = []
    #     MA.append(x[0])
    #     while i < len(x):
    #         window_average = (smoothening*x[i])+(1-smoothening)*MA[-1]
    #         MA.append(window_average)
    #         i += 1
    #     y[16 * t : 16 * (t + 1)] = MA
    #     t += 1
    #-------------------------------------------------#
    # chunk_size = 16
    # t = 0
    # window_size = 8
    # fixed = []
    # while t < CHUNK // chunk_size:
    #     x = temp[0 : chunk_size]
    #     i = 0
    #     MA = []
    #     while i < len(x) - window_size + 1:
    #         window_average = np.sum(x[i:i+window_size]) / window_size
    #         MA.append(window_average)
    #         i += 1
    #     fixed.append(MA)
    #     t += 1
    #-------------------------------------------------#
    
    # sos = signal.butter(4,400,fs=48000,output = 'sos')
    # y = signal.sosfilt(sos,x)
    zero_crossings = np.where(np.diff(np.sign(x)))[0]
    if len(zero_crossings) > 0:
        # time_between_crossings = zero_crossings[1:] - zero_crossings[:-1]
        time_between_crossings = np.diff(zero_crossings)
        avg_time_between_crossings = np.mean(time_between_crossings)
        freq = 48000 / avg_time_between_crossings / 2 #bagi 2 karena 1 crossing adalah setengah wave
        hitung.append(freq)
        if(len(hitung) == 10):
            freq = np.mean(hitung)
            print("%.2f Hz Zero-Crossing" %freq)
            hitung.clear()
    return freq
        # print("check = %.f"%check)
        # check += 1