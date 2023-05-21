'''
code write for project:
https://github.com/Ni3nayka/AVOCADO

author: Egor Bakay <egor_bakay@inbox.ru> Ni3nayka
write:  May 2022
modify: May 2023
'''
import tkinter

class my_keyboard:

    def __init__(self,extern_fun=None,window=None):
        self.window = window
        if self.window==None:
            self.window = tkinter.Tk()
        self.extern_fun = extern_fun
        if self.extern_fun==None:
            self.extern_fun = self._extern_fun_pass

        self.window.bind("<KeyPress>", self.key_handler)
        self.window.bind("<KeyRelease>", self.key_handler_off)

        if window==None:
            self.window.mainloop()

    def destroy(self):
        self.extern_fun = self._extern_fun_pass
        try:
            self.window.unbind("<KeyPress>")
            self.window.unbind("<KeyRelease>")
        except AttributeError: pass

    def key_handler(self,event):
        #print(event.char,event.keysym,event.keycode)
        self.extern_fun("+"+str(event.keycode))
    def key_handler_off(self,event):
        self.extern_fun("-"+str(event.keycode))
        
    def _extern_fun_pass(self,data):
        print(data)

if __name__ == "__main__":
    def test(a):
        print("qwerty:",a)
    keyboard = my_keyboard(test)