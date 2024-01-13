import socket
from threading import Thread
try: from device_interface import device_pass
except ModuleNotFoundError: from device.device_interface import device_pass

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
    
    def __init__(self,ip=None,port=1234,linux_mode=False):
        if ip==None: self.ip = get_ip()
        else: self.ip = ip
        self.port = port
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.linux_mode = linux_mode

    def write(self,data): 
        self.wifi_device.send(str(data+"\n").encode('utf-8'))

    def get(self): 
        return self.wifi_device_potok.get()
    
    def test(self):
        return (True,"ok")

    def start(self):
        # global global_kill_server
        # global_kill_server = False

        self.device.bind((self.ip, self.port))   
        self.device.listen(5) # Now wait for client connection.

        self.wifi_device, addr = self.device.accept() # тут ожидаем, пока не подключится
        print ('клиент подключился:', addr)

        self.wifi_device_potok = wifi_server_device_lisen(self.wifi_device)
        self.wifi_device_potok.start()

        # if self.linux_mode:
        #     self.wifi_device_test_connect = wifi_server_device_test_connect(self.wifi_device)
        #     self.wifi_device_test_connect.start()


    # def close(self):
    #     if self.linux_mode:
    #         # self.wifi_device_test_connect.stop()
    #         try: self.wifi_device_test_connect.stop()
    #         except AttributeError: 
    #             pass # инициализация не прошла полностью
    #             #print("wifi_device_test_connect - его нет")
    #     self.device.close()
    #     try: self.wifi_device_potok.stop()
    #     except AttributeError: pass # инициализация не прошла полностью

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
    test = wifi_device(linux_mode=True)
    sleep(1)
    print(test.get())
    test.write("123")
    test.write("1234")
    test.close()