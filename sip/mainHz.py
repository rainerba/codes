import numpy as np
import Servo
import audio
from time import sleep
from datetime import datetime

metode = "zeroC"
threshold= 2. #Hz

pSenar = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]
cek = False
pitch_before = 0.
hitung = 0

def ambil_data():
    x = audio.ambil_data()
    if metode == "yin":
        frek = Yin.main(x)
    elif metode == "fft":
        frek = FFT.main(x)
    elif metode == "zeroC":
        frek = Zero_Crossing.main(x)
    else:
        print("metode salah")
    return frek       
    
if __name__ == '__main__':
    if metode == "yin":
        import Yin
    elif metode == "fft":
        import FFT
    elif metode == "zeroC":
        import Zero_Crossing
    else:
        input("Metode salah, ketik yin, fft, atau zero_crossing")
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
            audio.stop()
            Servo.servo_stop()
            break
