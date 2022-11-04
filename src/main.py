from graphics.graphics import graphics,messagebox
from device.joystick import my_universal_joystick
from device.wifi_server import wifi_server_device

from threading import Thread
#from time import sleep

global_potok_flag = True

class potok(Thread):
    
    def __init__(self,port): 
        Thread.__init__(self)
        self.mem = 0
        self.port = port
    
    def run(self):
        gamepad = my_universal_joystick()
        wifi_device = wifi_server_device(self.port)
        
        if len(gamepad.joystick)+len(gamepad.button)+len(gamepad.arrow)==0:
            messagebox.showinfo("SaveSystem", "WARNING: Геймпад или не подключен или работает некорректно")

        while global_potok_flag:
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
                wifi_device.send(t)
            #sleep(0.05)
        wifi_device.close()
        

def test(command,data=""):
    global global_potok_flag
    if command=="start":
        global_potok_flag = True
        print(data)
        a = potok(int(data))
        a.start()
    else:
        global_potok_flag = False

window = graphics("AVOCADO beta version")
window.extern_fun = test
window.loop()
global_potok_flag = False