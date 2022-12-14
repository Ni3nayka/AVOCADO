from graphics.graphics import graphics,messagebox
from device.joystick import my_universal_joystick
from device.wifi_server import wifi_server_device

from threading import Thread
#from time import sleep

global_potok_flag = True
global_gamepad_flag = False
global_monitor_flag = False
global_connect_mode = "wi-fi" 
global_data_for_device_from_monitor = ""

class device_pass:
    def __init__(self): pass
    def close(self): pass

#wifi_device_array = []
global_device = device_pass()

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

        try:
            global global_potok_flag,global_data_for_device_from_monitor,global_gamepad_flag,global_monitor_flag#,wifi_device_array
            #global global_device
            gamepad = my_universal_joystick()

            if global_connect_mode=="wi-fi": global_device = wifi_server_device(self.port)
            #elif global_connect_mode=="bluetooth": device = wifi_server_device(self.port) ############
            else:
                messagebox.showerror("SaveSystem", "ERROR 7: неизвестный режим работы")
                return
            #wifi_device_array.append(device)
            global_device.start()

            window.del_expectation_viget()
            
            if len(gamepad.joystick)+len(gamepad.button)+len(gamepad.arrow)==0 and global_gamepad_flag:
                messagebox.showinfo("SaveSystem", "WARNING: Геймпад или не подключен или работает некорректно")

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
        except OSError:
            if global_potok_flag:
                messagebox.showerror("SaveSystem", "ERROR 11: ошибка сокета, предыдущий сеанс не был корректно завершен, пожалуйста перезапустите программу. Если это не помогло, перейдите на другой порт")
            else: print("ошибка => вылет потока, сеанс не был завершен")
        window.del_expectation_viget()

        print("2")
        global_device.close()
        try: global_device.close()
        except AttributeError: pass

        
# def stop_all_wifi_server():
#     for a in wifi_device_array:
#         a.close()

def test(command,data=""):
    global global_potok_flag,global_data_for_device_from_monitor,global_gamepad_flag,global_monitor_flag#,wifi_device_array

    if command.find("start")!=-1:

        if command.find("gamepad")!=-1: global_gamepad_flag = True
        else: global_gamepad_flag = False
        if command.find("monitor")!=-1: global_monitor_flag = True
        else: global_monitor_flag = False

        global_data_for_device_from_monitor = ""
        global_potok_flag = True
        print(data)
        a = potok(int(data))
        a.start()

    elif command=="monitor_message":
        global_data_for_device_from_monitor += data
        print(global_data_for_device_from_monitor)
    else: # stop
        global_data_for_device_from_monitor = ""
        global_potok_flag = False
        #stop_all_wifi_server()
        global_device.close()

window = graphics("AVOCADO v1.1")
window.extern_fun = test
window.loop()
global_potok_flag = False
#exit()
#stop_all_wifi_server()
global_device.close()