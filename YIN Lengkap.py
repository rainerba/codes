import numpy as np
from scipy.io import wavfile
# from scipy import signal
# import pyaudio

# RATE = 44100
# CHUNK = 1096
# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paFloat32,
#                 channels=1,
#                 rate=RATE,
#                 input=True,
#                 output=True,
#                 frames_per_buffer=CHUNK)

# def f(x):
#     f_0 = 1
#     envelope = lambda x: np.exp(-x)
#     return np.sin(x * np.pi * 2 * f_0) * envelope(x)

def ACF(f,W,t,lag):
    return np.sum(
        f[t : t+W] *
        f[lag+t: lag+t+W]
    )

def DF(f,W,t,lag):
    return ACF (f,W,t,0)\
    + ACF(f,W,t+lag,0)\
    - (2 * ACF (f,W,t,lag))

def CMNDF(f,W,t,lag): #cumulative mean normalized difference
    if lag == 0:
        return 1
    return DF(f,W,t,lag)\
    / np.sum([DF(f,W,t,j-1) for j in range (lag)]) * lag

def detect_pitch(f,W,t,sample_rate, bounds, thresh = 0.1):
    CMNDF_vals = [CMNDF(f,W,t,i) for i in range(*bounds)]
    sample = None
    for i, val in enumerate(CMNDF_vals):
        if val < thresh:
            sample = i + bounds[0]
            break
        if sample is None:
            sample = np.argmin(CMNDF_vals) + bounds[0]
    return sample_rate / sample

def main():
    sample_rate, data = wavfile.read("82.wav")
    data = np.float64(data)
    window_size = int(5/2000 * sample_rate)
    bounds = [20, 2000]
    
    pitches = []
    for i in range(data.shape[0] // (window_size + 3)):
        pitches.append(
            detect_pitch(
                data,
                window_size,
                i * window_size,
                sample_rate,
                bounds
            )
        )
    print(pitches)

main()

# while True:
#     try:
#         data = stream.read(CHUNK)
#         y = np.frombuffer(data, dtype=np.float32)
#         main()
#     except KeyboardInterrupt:
#         print('Stopped by user')
#         break