import socket
from threading import Thread
from tkinter import messagebox

def get_ip():
    answer = 0
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        answer = s.getsockname()[0]
        s.close()
    except Exception:
        return socket.gethostbyname(socket.gethostname())
    return answer

def kill_all_server(ip=None,port=12345,linux_mode=False):
    # создан для искуственного подключения к "серверу", чтобы он продолжил работу, а после отключения выключился,
    # тем самым выключив поток. возможно методы close уже нецелесообразны
    if ip==None: ip = get_ip()
    try:
        while 1:
            s = socket.socket()
            if linux_mode:
                s.settimeout(1)
            s.connect((ip, port))     
            # s.send(b'Hi i am aslam')
            # print(s.recv(1024))
            s.close()
    except ConnectionRefusedError: pass # сокеты кончились
    except TimeoutError: pass # сокеты на линуксе кончились

class wifi_server_device_lisen(Thread):

    def __init__(self,device):
        Thread.__init__(self)
        self.device = device 
        self.flag = True
        self.line = ""

    def stop(self):
        self.flag = False

    def run(self):
        self.device.settimeout(1.0)
        while self.flag:
            try: self.line += self.device.recv(1024).decode("utf-8")
            except socket.timeout: pass
            except ConnectionAbortedError: 
                print("хз что за проблема: Программа на вашем хост-компьютере разорвала установленное подключение")
                self.stop()

    def get(self):
        a = self.line
        self.line = ""
        return a

class wifi_server_device_test_connect(Thread):
    # https://ru.stackoverflow.com/questions/623982/Как-в-клиент-серверном-приложении-на-сокетах-узнать-что-клиент-завершил-соедине
    # https://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python

    def __init__(self,device):
        Thread.__init__(self)
        self.device = device 
        self.flag = True

    def stop(self):
        self.flag = False

    def run(self):
        while self.flag:
            try: 
                try: self.device.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT)
                except BlockingIOError: pass
                if self.flag:
                    print("клиент сказал - bye")
                self.stop()
                messagebox.showinfo("сообщение", "клиент отключился от сервера")
            except socket.timeout: pass # возможно это не надо....
            except ConnectionAbortedError: # и это тоже
                print("хз что за проблема: Программа на вашем хост-компьютере разорвала установленное подключение")
                self.stop()
            except AttributeError: # это точно надо
                self.stop()

class wifi_server_device:

    def __init__(self,port=1234,linux_mode=False):
        self.ip = get_ip()
        self.port = port
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.linux_mode = linux_mode

    def start(self):
        self.device.bind((self.ip, self.port))   
        self.device.listen(5) # Now wait for client connection.

        self.wifi_device, addr = self.device.accept() # тут ожидаем, пока не подключится
        print ('клиент подключился:', addr)

        self.wifi_device_potok = wifi_server_device_lisen(self.wifi_device)
        self.wifi_device_potok.start()

        if self.linux_mode:
            self.wifi_device_test_connect = wifi_server_device_test_connect(self.wifi_device)
            self.wifi_device_test_connect.start()

    def write(self,data):
        self.wifi_device.send(str(data+"\n").encode('utf-8'))

    def get(self):
        return self.wifi_device_potok.get()

    def close(self):
        print("!!!!!!!!!!111!!11!!!!!11!")
        if self.linux_mode:
            try: self.wifi_device_test_connect.stop()
            except AttributeError: pass # инициализация не прошла полностью
        self.device.close()
        try: self.wifi_device_potok.stop()
        except AttributeError: pass # инициализация не прошла полностью

if __name__=="__main__":
    from time import sleep
    test = wifi_server_device()
    test.start()
    for i in range(10):
        test.write(str(i))
        sleep(0.1)
    print(test.get())
    print("end")
    test.close()
    #sleep(10)
    #close_all_server()


