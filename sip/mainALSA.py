import pyalsaaudio
import array
import numpy as np
import Servo
import Yin
import FFT
import Zero_Crossing

CHUNK = 2048
MIC = 2
p = alsaaudio.PCS(type=alsaaudio.PCM_CAPTURE)
p.setchannels(1)
p.setrate(48000)
p.setformat(alsaaudio.PCM+FORMAT_FLOAT_LE)
p.setperiodsize(CHUNK)

if __name__ == '__main__':
    buffer = array.array('f')

    pilih_senar = [329.63, 246.94, 196.00, 146.83, 110.00, 82.41]
    #senar = input("Pilih senar yang akan diatur: ") - 1
    senar = 1
    cek = False
    metode = "yin"
    pitch_before = 0.
    while True:
        try:
            buffer.fromstring(p.read()[2])
            data = np.array(buffer, dtype='f')
            x = data.copy()
            if metode == "yin":
                frek = Yin.process_audio(x)
            elif metode == "fft":
                frek = FFT.estimate_frequency(x)
            elif metode == "zero_crossing":
                frek = Zero_Crossing.main(data)
            else:
                input("Metode salah, ketik yin, fft, atau zero_crossing")
                
            if np.abs(pitch_before - frek) < 5. and frek > 0:
                print(frek)
                cek = True
            pitch_before = frek
                

            if cek:
                Servo.start_servo()
                if frek < pilih_senar[senar]:
                    Servo.CW()
                elif frek > pilih_senar[senar]:
                    Servo.CCW()
                elif pilih_senar[senar] - 5 <= frek >= pilih_senar[senar] + 5:
                    Servo.servo_stop()

        except KeyboardInterrupt:
            print("Program Berhenti")
            break