import numpy as np

# Optimized functions for Real Time - LESM (Ledesma-Smolkin / Less Math)
# Note detect funtions only need recieve the data from t to t + W + lagMax
 
def ACF_lesm(f, W, t, lag):
    corr = np.correlate(f[t : t + W], f[t + lag : t + lag + W], mode = 'valid') #corr: makin banyak kesamaan, makin tinggi nilai
    return corr[0]

def DF_lesm(f, W, lag):
    return ACF_lesm(f, W, 0, 0) + ACF_lesm(f, W, lag, 0) - (2 * ACF_lesm(f, W, 0, lag))

# Optimized Algorithm without Parabolic Interpolation or Best Local Estimate
def detect_pitch_lesm(f, W, bounds, thresh=0.1):
    lag_max = bounds[1]
    running_sum = 0
    vals = [1]
    sample = None

    for lag in range(1, lag_max): #1-640
        # Difference Function
        dfResult = DF_lesm(f, W, lag)
        # Memoized Cumulative Mean Normalized Difference Function
        running_sum += dfResult
        val = dfResult / running_sum * lag
        vals.append(val)
        # Absolute Thresholding with short-stopping
        if lag >= bounds[0] and val < thresh:
            sample = lag
            break
    # No acceptable lag found, default to minimum error
    else:
        argmin = np.argmin(vals)
        sample = argmin if argmin > bounds[0] else bounds[0]

    return 48000 / sample

# Optimized Algorithm with Parabolic Interpolation
def detect_pitch_interpolated_lesm(f, W, bounds, thresh=0.1):
    lag_max = bounds[1]
    running_sum = 0
    vals = [1]

    for lag in range(1, lag_max):
        # Difference Function
        dfResult = DF_lesm(f, W, lag)
        # Memoized Cumulative Mean Normalized Difference Function
        running_sum += dfResult
        val = dfResult / running_sum * lag
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

def process_audio(data,fmin, fmax, windows_size=1024, method='lesm'):
    lagMin = int(1/fmax * 48000) #1/500 * 48000 = 96
    lagMax = int(1/fmin * 48000) #1/75 * 48000 = 640
    bounds = [lagMin,lagMax]

    if method == 'lesm':
        pitches = []
        for i in range(data.shape[0] // (windows_size+3)): #32384 // 131 = 247
            t = i*windows_size                             #247 * 128 = 31.616
            pitches.append(detect_pitch_lesm(f=data[t : t + windows_size + lagMax], W=windows_size, bounds=bounds))
        return pitches

    elif method == 'lesm-i':
        t = windows_size
        return detect_pitch_interpolated_lesm(f=data[t : t + windows_size + lagMax], W=windows_size, bounds=bounds)
    #coba t awal diubah jadi 0
    else:
        raise ValueError(f'Invalid method: {method}')

def lesm_main(x):
    pitch_before = 0.
    pitch_now = 0.
    #CHUNK = 2048 #jangan dioatak atik
    while True:
        try:
            metode = 'lesm-i'
            pitch_now = process_audio(data = x, fmin=75, fmax=500, windows_size=1024, method=metode)
            if np.abs(pitch_before - pitch_now) < 5.:
                print(pitch_now, "Hz", metode)
                return pitch_now
            pitch_before = pitch_now
        except KeyboardInterrupt:
            print('Stopped by user')
            break