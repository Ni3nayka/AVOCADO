try:
    from graphics.graphics import graphics, messagebox
    from device.joystick import my_universal_joystick
    from device.wifi_server import wifi_server_device, kill_all_server
    from device.keyboard import my_keyboard
    from device.serial_driver import arduino_usb
    from threading import Thread
    from sys import platform
except ModuleNotFoundError as e:
    print(e)
    from time import sleep
    print("ERROR IMPORT PYTHON LIB!!!")
    print("if you use linux, run install.sh")
    print("=====================================")
    raise
# from time import sleep

global_potok_flag: bool = True
global_gamepad_flag = False
global_monitor_flag = False
global_keyboard_flag = False
global_connect_mode = "wi-fi" 
global_data_for_device_from_monitor = ""
global_last_port = 1234

global_linux_mode = platform.upper().find("LINUX")>-1 # True = Linux, false = Windows

class device_pass:
    def __init__(self): pass
    def close(self): pass
    def destroy(self): pass

global_device = device_pass()
global_keyboard = device_pass()

class potok(Thread):
    
    def __init__(self,port): 
        Thread.__init__(self)
        self.mem = 0
        self.port = port
    
    def run(self):
        #device = 0
        global_device = 0
        # эта хрень должна быть глобальной, чтобы если не было подключения ее можно было отключить
        # эта хрень должна быть локальной, чтобы при подключении она сама могла отключаться
        global global_potok_flag, global_data_for_device_from_monitor, global_gamepad_flag, global_monitor_flag, global_keyboard_flag, global_keyboard  # ,wifi_device_array
        try:
            #global global_device
            #kill_all_server(port=self.port)

            gamepad = my_universal_joystick()
            if len(gamepad.joystick)+len(gamepad.button)+len(gamepad.arrow)==0 and global_gamepad_flag:
                messagebox.showinfo("SaveSystem", "WARNING: Геймпад или не подключен или работает некорректно")
                #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") # 11:11:11:11:11:11
            
            if global_connect_mode=="wi-fi": global_device = wifi_server_device(self.port)
            #elif global_connect_mode=="bluetooth": device = bluetooth_device(self.port) ############
            elif global_connect_mode=="serial": 
                global_device = arduino_usb(self.port) # ,baud=9600
                if not global_device.enable: 
                    messagebox.showerror("SaveSystem", "Не удалось подключиться к устройству на порте " + self.port)
                    global_potok_flag = False
            else:
                messagebox.showerror("SaveSystem", "ERROR 7: неизвестный режим работы")
                return
            global_device.start()

            window.del_expectation_viget()

            def keyboard_fun(data):
                global_device.write(data)
            global_keyboard = my_keyboard(keyboard_fun,window.window)
            if not global_keyboard_flag:
                global_keyboard.destroy()

            while global_potok_flag:

                if global_gamepad_flag:
                    gamepad.update()
                    j = []
                    for i in gamepad.joystick:
                        j.append(int(i*100))
                    a = []
                    for i in gamepad.arrow:
                        for ii in i:
                            a.append(ii)
                    t = "{ joystick: " + ' '.join(map(str,j)) + " button: " +''.join(map(str,gamepad.button)) + " arrow: " +' '.join(map(str,a)) + " }"
                    if t!=self.mem:
                        self.mem = t
                        #print(self.mem)
                        global_device.write(t)

                if global_monitor_flag:
                    data = global_device.get()
                    if data!="":
                        window.add_line_to_text_monitor_viget(data)
                    if global_data_for_device_from_monitor!="":
                        if global_gamepad_flag:
                            a = global_data_for_device_from_monitor
                            global_data_for_device_from_monitor = global_data_for_device_from_monitor.replace('{','').replace('}','')
                            if a!=global_data_for_device_from_monitor:
                                messagebox.showinfo("SaveSystem", "Символы '{' и '}' не отправляются данном режиме работы т.к. они нужны для работы геймпада")
                        global_device.write(global_data_for_device_from_monitor)
                        global_data_for_device_from_monitor = ""

                #sleep(0.05)
            global_device.close()
            global_keyboard.destroy()
            kill_all_server(port=self.port,linux_mode=global_linux_mode)
        except OSError:
            if global_potok_flag:
                messagebox.showerror("SaveSystem", "ERROR 11: ошибка сокета, предыдущий сеанс не был корректно завершен, пожалуйста перезапустите программу. Если это не помогло, перейдите на другой порт")
            else: print("ошибка => вылет потока, сеанс не был завершен")
        window.del_expectation_viget()

        print("2")
        global_device.close()
        try: global_device.close()
        except AttributeError: pass

def test(command,data=""):
    global global_potok_flag,global_data_for_device_from_monitor,global_gamepad_flag,global_monitor_flag,global_last_port,global_keyboard_flag,global_connect_mode#,wifi_device_array

    if command.find("start")!=-1:

        if command.find("gamepad")!=-1: global_gamepad_flag = True
        else: global_gamepad_flag = False
        if command.find("monitor")!=-1: global_monitor_flag = True
        else: global_monitor_flag = False
        if command.find("keyboard")!=-1: global_keyboard_flag = True
        else: global_keyboard_flag = False

        if command.find("wi-fi")!=-1: global_connect_mode = "wi-fi"
        elif command.find("bluetooth")!=-1: global_connect_mode = "bluetooth"
        elif command.find("serial")!=-1: global_connect_mode = "serial"
        else: 
            messagebox.showerror("SaveSystem", "ERROR 7(1): неизвестный режим работы")
            return

        global_data_for_device_from_monitor = ""
        global_potok_flag = True
        print(data)
        try: global_last_port = int(data)
        except ValueError: global_last_port = data
        a = potok(global_last_port)
        a.start()

    elif command=="monitor_message":
        global_data_for_device_from_monitor += data
        print(global_data_for_device_from_monitor)
    else: # stop
        global_data_for_device_from_monitor = ""
        global_potok_flag = False
        window.del_expectation_viget()
        global_device.close()
        global_keyboard.destroy()
        kill_all_server(port=global_last_port,linux_mode=global_linux_mode)

window = graphics("AVOCADO v1.3 beta",linux_mode=global_linux_mode)
window.extern_fun = test
window.loop()
global_potok_flag = False
global_device.close()
kill_all_server(port=global_last_port,linux_mode=global_linux_mode)
#if global_linux_mode: exit()