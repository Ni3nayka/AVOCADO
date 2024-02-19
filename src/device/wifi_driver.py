import socket
from threading import Thread
try: from device_interface import device_pass
except ModuleNotFoundError: from device.device_interface import device_pass
import errno

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

class wifi_device(Thread,device_pass):
    
    def __init__(self,ip=None,port=1234): # ,linux_mode=False
        # setup
        Thread.__init__(self)
        device_pass.__init__(self,True)
        if ip==None: self.ip = get_ip()
        else: self.ip = ip
        self.port = int(port)
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # https://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
        # self.linux_mode = linux_mode
        self.enable = True
        self.line = ""
        self.test_message = self.DEVICE_SETUP
        # start connect thread
        self.start()

    def write(self,data): 
        if not self.enable: return
        self.wifi_device.send(str(data+"\n").encode('utf-8'))

    def get(self): 
        a = self.line
        self.line = ""
        return a
    
    def test(self):
        return self.test_message
    
    def close(self):
        print("close", self.enable)
        if not self.enable: return
        self.enable = False
        try: self.wifi_device.close()
        except AttributeError: pass
        self.device.close()
        # kill server (кусок от старой версии, если сервера не будут выключаться, расскоментить)
        try:
            while 1:
                s = socket.socket()
                s.settimeout(0.2) #if self.linux_mode:
                s.connect((self.ip, self.port))     
                s.close()
        except ConnectionRefusedError: pass # сокеты кончились
        except ConnectionResetError: pass # сокеты на линуксе кончились
        except TimeoutError: pass # сокеты на линуксе кончились

    def run(self):
        # connect
        try: self.device.bind((self.ip, self.port))   
        except OSError: 
            self.test_message = "Порт занят, попробуйте другой порт"
            print(self.test_message)
            self.close()
            return
        self.device.listen(5) # Now wait for client connection.
        self.wifi_device, addr = self.device.accept() # тут ожидаем, пока не подключится
        print ('клиент подключился:', addr)
        self.test_message = self.DEVICE_OK
        # loop
        self.wifi_device.settimeout(1.0) # таймаут для опроса по wifi
        while self.enable:
            # получаем информацию с wifi
            try: 
                data = self.wifi_device.recv(1024)
                print(data)
                try: self.line += data.decode("utf-8")
                except UnicodeDecodeError: self.line += data.decode("utf-16")
                except: self.line += "???????????????????????????????"
            except socket.timeout: pass
            except ConnectionAbortedError: 
                print("хз что за проблема: Программа на вашем хост-компьютере разорвала установленное подключение")
                self.close()
                self.test_message = "Программа на вашем хост-компьютере разорвала установленное подключение"
            except OSError: pass # скорее всего уже отключили...
            # проверяем, девайс еще живой или нет
            if self.enable: # https://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python
                try:
                    buf = self.wifi_device.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT)
                    if buf == b'':
                        if self.enable:
                            self.test_message = "Клиент прервал соединение"
                        self.close()
                except BlockingIOError as exc:
                    if exc.errno != errno.EAGAIN:
                        # Raise on unknown exception
                        # raise
                        pass
                except TimeoutError: pass
                except OSError: pass
            print("контакт с клиентом:",self.test_message)
        print("поток wifi закрылся")

if __name__=="__main__":
    # from time import sleep
    # test = wifi_server_device()
    # test.start()
    # for i in range(10):
    #     test.write(str(i))
    #     sleep(0.1)
    # print(test.get())
    # print("end")
    # test.close()
    # #sleep(10)
    # #close_all_server()

    # test = wifi_server_device(port=1234,linux_mode=True)
    # test.start()
    # test.close()
    # kill_all_server(port=1234,linux_mode=True)

    from time import sleep
    test = wifi_device() # linux_mode=True
    # test.start()
    sleep(3)
    print(test.get())
    test.write("123")
    sleep(1)
    test.write("123")
    sleep(1)
    test.write("123")
    test.write("123")
    test.write("1234")
    test.close()
    print("end")