import pyaudio
import numpy as np
# import Servo
import Yin
import FFT
import Zero_Crossing

RATE = 48000
CHUNK = 2048 #jangan dioatak atik
p = pyaudio.PyAudio()

if __name__ == '__main__':
    stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

    pilih_senar = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]
    senar = int(input("Pilih senar yang akan diatur: ")) - 1
    cek = False
    metode = "yin"
    while True:
        try:
            y = stream.read(CHUNK, exception_on_overflow = False)
            data = np.frombuffer(y, dtype=np.float32)
            x = data.copy()
            if metode == "yin":
                frek = Yin.lesm_main(x)
                cek = True
            elif metode == "fft":
                frek = FFT.estimate_frequency(x)
                cek = True
            elif metode == "zero_crossing":
                frek = Zero_Crossing.main(x)
                cek = True
            else:
                input("Metode salah, ketik yin, fft, atau zero_crossing")

            if cek:
                if frek < pilih_senar[senar]:
                    # Servo.CW()
                    print("naik")
                elif frek > pilih_senar[senar]:
                    # Servo.CCW()
                    print("turun")
                elif pilih_senar[senar] - 5 <= frek >= pilih_senar[senar] + 5:
                    # Servo.servo_stop()6
                    print("ok")

        except KeyboardInterrupt:
            print("Program Berhenti")
            break