import socket

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

    def send(self,data):
        self.wifi_device.send(str(data+"\n").encode('utf-8'))

    def close(self):
        self.device.close()

if __name__=="__main__":
    from time import sleep
    test = wifi_server_device()
    for i in range(10):
        test.send(str(i))
        #sleep(1)
    test.close()


