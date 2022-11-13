import socket
from threading import Thread

class wifi_server_device_lisen(Thread):

    def __init__(self,device):
        Thread.__init__(self)
        self.device = device 
        self.flag = True

    def run(self):
        while self.flag:
            print(self.device.recv(1024))

    def stop(self):
        self.flag = False

class wifi_server_device:

    def __init__(self,port=12345):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.device = socket.socket()
        self.device.bind((self.ip, self.port))   
        self.device.listen(5) # Now wait for client connection.

        self.wifi_device, addr = self.device.accept()
        #print ('Got connection from', addr)
        #print (self.wifi_device.recv(1024))

        self.wifi_device_potok = wifi_server_device_lisen(self.wifi_device)
        self.wifi_device_potok.start()

    def send(self,data):
        self.wifi_device.send(str(data+"\n").encode('utf-8'))

    def close(self):
        self.device.close()
        self.wifi_device_potok.stop()

if __name__=="__main__":
    from time import sleep
    test = wifi_server_device()
    for i in range(10):
        test.send(str(i))
        #sleep(1)
    test.close()


