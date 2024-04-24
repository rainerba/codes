import pyaudio
import numpy as np
import psutil
import Servo
from time import sleep
from datetime import datetime

metode = "fft"
threshold= 0.1 #toleransi frekuensi dalam Hz
CHUNK = 8192

pSenar = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]
p = pyaudio.PyAudio()
cek = False
pitch_before = 0.
hitung = 0
MIC = 1
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=48000,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index = MIC)

def select_microphone(index):
    device_info = p.get_device_info_by_index(index)
    if device_info.get('maxInputChannels') > 0:
        print("Selected Microphone:", device_info.get('name'))
    else:
        print("No microphone at index ", index)

def ambil_data():
    y = stream.read(CHUNK, exception_on_overflow = False)
    data = np.frombuffer(y, dtype=np.float32)
    x = data.copy()
    if metode == "yin":
        import Yin
        frek = Yin.process_audio(x)
    elif metode == "fft":
        import FFT
        frek = FFT.estimate_frequency(x)
    elif metode == "zeroC":
        import Zero_Crossing
        frek = Zero_Crossing.main(data)
    else:
        input("Metode salah, ketik yin, fft, atau zero_crossing")
    return frek    
    
if __name__ == '__main__':
    select_microphone(MIC)
    print("Threshold: ", threshold, "Hz")
    senar = int(input("Pilih senar yang akan diatur: ")) - 1
    Servo.start_servo()
    print("mulai genjreng")
    start = datetime.now()
    while True:
        try:
            frek = ambil_data()   
            pitch_before = frek
            beda = frek - pSenar[senar]
            if np.abs(beda) < 30: #ubah kalo terlalu banyak noise yang kedetect
                print("beda", beda)
                print(frek, "Hz")
                if Servo.main(beda, threshold):
                    print("Sudah sesuai threshold!")
                    hitung += 1
                    Servo.hold()
                    sleep(0.1)
                    if hitung == 2: #ubah kalo terlalu hoki
                        end = datetime.now()
                        print((end - start).total_seconds())
                        senar = int(input("Senar? ")) - 1
                        hitung = 0
                        start = datetime.now()
                else: #untuk memastikan perhitungan bukan ((hoki))
                    hitung = 0
            else: #kalo beda > 30
                Servo.hold()

        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            Servo.servo_stop()
            print(" Program Berhenti")
            break
