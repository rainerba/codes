import pyaudio
import numpy as np

MIC = 1
CHUNK = 8192
RATE = 48000
p =  pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
            channels=1,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK,
            input_device_index = MIC)

def select_microphone(index):
    device_info = p.get_device_info_by_index(index)
    if device_info.get('maxInputChannels') > 0:
        print("Selected Microphone:", device_info.get('name'))
    else:
        print("No microphone at index ", index)

select_microphone(MIC)

def ambil_data():
    y = stream.read(CHUNK, exception_on_overflow = False)
    data = np.frombuffer(y, dtype=np.float32)
    x = data.copy()
    x -= np.mean(x)
    return x

def stop():
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Program Berhenti")