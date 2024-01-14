try:
    from device.device_interface import device_pass
    from device.wifi_driver import wifi_device, get_ip
    from device.serial_driver import arduino_usb
    from user.joystick import my_universal_joystick
    from user.keyboard import my_keyboard
    from graphics.graphics import graphics, messagebox
    from threading import Thread
    from sys import platform
    from time import sleep
except ModuleNotFoundError as e:
    print(e)
    print("ERROR IMPORT PYTHON LIB!!!")
    print("if you use linux, run install.sh")
    print("=====================================")
    raise

class keyboard_pass(device_pass):
    def destroy(self): pass
class global_data:
    def __init__(self):
        # const
        self.ip:str = get_ip()
        self.linux_mode:bool = platform.upper().find("LINUX")>-1 # True = Linux, false = Windows
        # flag and save
        self.potok_flag:bool = True
        self.gamepad_flag:bool = False
        self.monitor_flag:bool = False
        self.keyboard_flag:bool = False
        self.connect_mode:str = "wi-fi" 
        self.data_for_device_from_monitor:str = ""
        self.port = 1234 # last_port
        # object
        self.device = device_pass()
        self.keyboard = keyboard_pass()
DATA = global_data()

class potok(Thread):
    
    def __init__(self,data): 
        Thread.__init__(self)
        self.joystick_save = 0
        self.DATA:global_data = data
        self.start()
    
    def run(self):
        # запускаем девайсы и ожидаем ото всех контакт
        # self.DATA.device = device_pass()
        gamepad = my_universal_joystick()
        if len(gamepad.joystick)+len(gamepad.button)+len(gamepad.arrow)==0 and self.DATA.gamepad_flag:
            messagebox.showinfo("SaveSystem", "WARNING: Геймпад или не подключен или работает некорректно")
        if self.DATA.connect_mode=="wi-fi": 
            self.DATA.device = wifi_device(ip=self.DATA.ip,port=self.DATA.port) # ,linux_mode=self.DATA.linux_mode
        elif self.DATA.connect_mode=="bluetooth": 
            messagebox.showerror("SaveSystem", "Блютуз пока не работает, доделаю в следующей версии :)\n(но это не точно)")
            #device = bluetooth_device(self.DATA.port) ############ 12:12:12:12:12:12
            self.DATA.potok_flag = False
        elif self.DATA.connect_mode=="serial": 
            self.DATA.device = arduino_usb(self.DATA.port[0],self.DATA.port[1]) # ,baud=9600
            if not self.DATA.device.enable: 
                messagebox.showerror("SaveSystem", "Не удалось подключиться к устройству на порте " + str(self.DATA.port))
                self.DATA.potok_flag = False
        else:
            messagebox.showerror("SaveSystem", "ERROR 7: неизвестный режим работы")
            return
        # setup
        while self.DATA.potok_flag and self.DATA.device.test()==self.DATA.device.DEVICE_SETUP: sleep(0.2)
        # удаляем иконку ожидания (все готово или не было контакта от кого-то)
        window.del_expectation_viget()
        # keyboard
        def keyboard_fun(data):
            self.DATA.device.write(data)
        if self.DATA.keyboard_flag:
            self.DATA.keyboard = my_keyboard(keyboard_fun,window.window)
        # loop
        while self.DATA.potok_flag:
            # геймпад
            if self.DATA.gamepad_flag:
                gamepad.update()
                j = []
                for i in gamepad.joystick:
                    j.append(int(i*100))
                a = []
                for i in gamepad.arrow:
                    for ii in i:
                        a.append(ii)
                t = "{ joystick: " + ' '.join(map(str,j)) + " button: " +''.join(map(str,gamepad.button)) + " arrow: " +' '.join(map(str,a)) + " }"
                if t!=self.joystick_save:
                    self.joystick_save = t
                    #print(self.mem)
                    self.DATA.device.write(t)
            # монитор
            if self.DATA.monitor_flag:
                data = self.DATA.device.get()
                if data!="":
                    window.add_line_to_text_monitor_viget(data)
                if self.DATA.data_for_device_from_monitor!="":
                    if self.DATA.gamepad_flag:
                        a = self.DATA.data_for_device_from_monitor
                        self.DATA.data_for_device_from_monitor = self.DATA.data_for_device_from_monitor.replace('{','').replace('}','')
                        if a!=self.DATA.data_for_device_from_monitor:
                            messagebox.showinfo("SaveSystem", "Символы '{' и '}' не отправляются данном режиме работы т.к. они нужны для работы геймпада")
                    self.DATA.device.write(self.DATA.data_for_device_from_monitor)
                    self.DATA.data_for_device_from_monitor = ""
            # чтобы старые ведра не умирали при запуске этого ПО
            sleep(0.05) 
        # закрываем поток
        self.DATA.device.close()
        self.DATA.keyboard.destroy()
        print("конец потока обработчика сеанса")

def test(command,data=""):
    if command.find("start")!=-1:
        # user device
        if command.find("gamepad")!=-1: DATA.gamepad_flag = True
        else: DATA.gamepad_flag = False
        if command.find("monitor")!=-1: DATA.monitor_flag = True
        else: DATA.monitor_flag = False
        if command.find("keyboard")!=-1: DATA.keyboard_flag = True
        else: DATA.keyboard_flag = False
        # device
        if command.find("wi-fi")!=-1: DATA.connect_mode = "wi-fi"
        elif command.find("bluetooth")!=-1: DATA.connect_mode = "bluetooth"
        elif command.find("serial")!=-1: DATA.connect_mode = "serial"
        else: 
            messagebox.showerror("SaveSystem", "ERROR 7(1): неизвестный режим работы")
            return
        # start thread
        DATA.data_for_device_from_monitor = ""
        DATA.potok_flag = True
        print("порт для запуска:",data)
        DATA.port = data
        potok(DATA)
    elif command=="monitor_message":
        DATA.data_for_device_from_monitor += data
        print("монитор (отправить):",DATA.data_for_device_from_monitor)
    else: # stop
        DATA.data_for_device_from_monitor = ""
        DATA.potok_flag = False
        DATA.device.close()
        DATA.keyboard.destroy()
        window.del_expectation_viget()

window = graphics("AVOCADO v2.0 beta",linux_mode=DATA.linux_mode)
window.extern_fun = test
window.loop()
DATA.potok_flag = False
DATA.device.close()
print("КОНЕЦ")