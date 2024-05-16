import numpy as np
import psutil
import Servo
import audio
from time import sleep
from datetime import datetime

metode = "yin"
threshold= 0.5 # persen

pSenar = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]
hitung = 0
ps = psutil.Process()
cpu_persen = []

def ambil_data(senar):
    x = audio.ambil_data()
    if metode == "yin":
        frek = Yin.main(x)
    elif metode == "fft":
        frek = FFT.main(x)
    elif metode == "zeroC":
        frek = Zero_Crossing.main(x, senar)
    else:
        frek = 0.
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
    print("Metode: ", metode)
    print("Threshold: ", threshold, "persen")
    senar = int(input("Pilih senar yang akan diatur: ")) - 1
    Servo.start_servo()
    print("mulai genjreng")
    start = datetime.now()
    while True:
        try:
            frek = ambil_data(senar)
            with ps.oneshot():
                cpu_persen.append(ps.cpu_percent())
                memori = ps.memory_full_info()
            beda = frek - pSenar[senar]
            if np.abs(beda) < 30: # <20 karena +100 cents senar 1 = 19.6 Hz, dan error rate 50%
                print("beda", beda)
                print(frek, "Hz")
                if Servo.main(beda, pSenar[senar] * threshold / 100, senar):
                    print("Sudah sesuai threshold!")
                    hitung += 1
                    Servo.hold()
                    sleep(0.1)
                    if hitung == 2: #ubah kalo terlalu hoki
                        end = datetime.now()
                        hasil = (end - start).total_seconds()
                        print(hasil, "detik")
                        cpu = np.mean(cpu_persen)
                        print(cpu, "cpu")
                        cpu_persen = []
                        hitung = 0
                        senar = int(input("Senar? ")) - 1
                        start = datetime.now()
                else: #untuk memastikan perhitungan bukan ((hoki))
                    hitung = 0
            else: #kalo beda > 20
                Servo.hold()

        except KeyboardInterrupt:
            audio.stop()
            Servo.servo_stop()
            break
