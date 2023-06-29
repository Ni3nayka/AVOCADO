'''
code write for project:
https://github.com/Ni3nayka/AVOCADO

author: Egor Bakay <egor_bakay@inbox.ru> Ni3nayka
write:  June 2023
modify: June 2023

info:
pip install pyserial

example:
arduino = serial.Serial("COM11",9600)
print(arduino.in_waiting)
print(arduino.readline())
arduino.write(b'hello')
arduino.close()
'''

import serial
from threading import Thread

class arduino_usb(Thread):
    
    def __init__(self,com,baud=9600): # com = 'com6' "/dev/ttyUSB0"
        Thread.__init__(self)
        self.ser = 0
        self.enable = 1
        try: self.ser = serial.Serial(com,baud)
        except serial.serialutil.SerialException:
            self.enable = 0
            print("ERROR <arduino_usb>: no USB device:", com)
    
    # def now_read(self):
    #     if (not self.enable): return 0
    #     S = self.ser.readline()
    #     # b'1\r\n' => 1
    #     #print(S, " ", end='')
    #     # отрезаем "мусор"
    #     S = str(S)
    #     S = list(S)  # str => mas
    #     del S[0]
    #     del S[0]
    #     del S[len(S)-1]
    #     del S[len(S)-1]
    #     del S[len(S)-1]
    #     del S[len(S)-1]
    #     del S[len(S)-1]
    #     S = ''.join(S) # mas => str
    #     #print(S)
    #     return S

    # def write(self,S):
    #     if (not self.enable): return 0
    #     #ser.write(b'hello, arduino!!!\n') # \r
    #     S = str(S)
    #     S1 = bytearray(b'')
    #     i = 0
    #     while (i<len(S)):
    #         S1.append(ord(S[i]))
    #         i += 1
    #     S1.append(ord('\n'))
    #     #print(bytes(S1))
    #     self.ser.write(S1)
    
    # def run(self): # Запуск потока
    #     if not self.enable: return 0
    #     while 1:
    #         S = self.ser.readline()
    #         print(S, " ", end='')
    #         S = str(S)
    #         S = list(S)  # str => mas
    #         del S[0]
    #         del S[0]
    #         del S[len(S)-1]
    #         del S[len(S)-1]
    #         del S[len(S)-1]
    #         del S[len(S)-1]
    #         del S[len(S)-1]
    #         S = ''.join(S) # mas => str
    #         print(S)
            
    # def available(self):
    #     if (not self.enable): return 0
    #     if (len(self.mas)>0):
    #         return 1
    #     else:
    #         return 0
        
    # def read(self):
    #     if (not self.enable): return 0
    #     if (len(self.mas)>0):
    #         S = self.mas[0]
    #         del self.mas[0]
    #         return S
    #     else:
    #         return 0
        
    # def wait_read(self):
    #     if (not self.enable): return 0
    #     while (len(self.mas)==0): pass
    #     S = self.mas[0]
    #     del self.mas[0]
    #     return S

    def start(self): pass

    def write(self,data):
        if (not self.enable): return None
        self.ser.write(str(data+"\n").encode('utf-8'))

    def get(self):
        if not self.enable: return 0
        a = b''
        while self.ser.in_waiting: a += self.ser.read()
        return a.decode('utf-8')

    def close(self):
        try: self.ser.close()
        except: pass


if __name__ == "__main__":
    from time import sleep
    test = arduino_usb("COM8")
    test.start()
    print(test.enable)
    for i in range(4):
        test.write(str(i))
        sleep(1)
    print(test.get())
    print("end")
    test.close()
