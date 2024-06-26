import numpy as np

# Optimized functions for Real Time - LESM (Ledesma-Smolkin / Less Math)
# Note detect funtions only need recieve the data from t to t + W + lagMax
 
def ACF_lesm(f, W, t, lag):
    corr = np.correlate(f[t:t+W], f[t+lag:t+lag+W], mode='valid')
    return corr[0]

def DF_lesm(f, W, lag):
    return ACF_lesm(f,W,0,0)+ACF_lesm(f,W,lag,0)-(2*ACF_lesm(f,W,0,lag))

# Optimized Algorithm with Parabolic Interpolation
def detect_pitch_interpolated_lesm(f, W, bounds, thresh=0.1):
    running_sum = 0
    vals = [1]

    for lag in range(1, 640):
        # Difference Function
        dfResult = DF_lesm(f, W, lag)
        # Memoized Cumulative Mean Normalized Difference Function
        running_sum += dfResult
        val = (dfResult / running_sum) * lag
        vals.append(val)
        # Absolute Thresholding with short-stopping
        if lag >= bounds[0] and val < thresh:
            sample = lag
            break
    # No acceptable lag found, default to minimum error
    else:
        sample = np.argmin(vals[bounds[0]:]) + bounds[0]
    # Parabolic interpolation
    if 1 < sample < len(vals) - 1:
        s0, s1, s2 = vals[sample-1], vals[sample], vals[sample+1]
        correction = 0.5 * (s2 - s0) / (2 * s1 - s2 - s0)
        sample += correction
    return 48000 / sample

def main(data,fmin=75, fmax=400, windows_size=1024):
    lagMin = 48000//fmax #= 120
    lagMax = 48000//fmin #= 640
    bounds = [lagMin,lagMax]
    hasil = detect_pitch_interpolated_lesm(f=data, W=windows_size, bounds=bounds)
    return hasil

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