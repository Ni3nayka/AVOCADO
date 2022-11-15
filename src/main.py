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

class potok(Thread):
    
    def __init__(self,port): 
        Thread.__init__(self)
        self.mem = 0
        self.port = port
    
    def run(self):
        global global_potok_flag,global_data_for_device_from_monitor,global_gamepad_flag,global_monitor_flag
        gamepad = my_universal_joystick()

        device = 0
        if global_connect_mode=="wi-fi": device = wifi_server_device(self.port)
        #elif global_connect_mode=="bluetooth": device = wifi_server_device(self.port) ############
        else:
            messagebox.showerror("SaveSystem", "ERROR 7: неизвестный режим работы")
            return
        
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
                    print(self.mem)
                    device.write(t)

            if global_monitor_flag:
                data = device.get()
                if data!="":
                    window.add_line_to_text_monitor_viget(data)
                if global_data_for_device_from_monitor!="":
                    device.write(global_data_for_device_from_monitor)
                    global_data_for_device_from_monitor = ""
                
            #sleep(0.05)
        device.close()
        print("!")
        

def test(command,data=""):
    global global_potok_flag,global_data_for_device_from_monitor,global_gamepad_flag,global_monitor_flag

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
    else:
        global_data_for_device_from_monitor = ""
        global_potok_flag = False

window = graphics("AVOCADO beta version")
window.extern_fun = test
window.loop()
global_potok_flag = False
exit()