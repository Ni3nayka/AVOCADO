'''
code write for project:
https://github.com/Ni3nayka/AVOCADO

author: Egor Bakay <egor_bakay@inbox.ru> Ni3nayka
write:  May 2022
modify: May 2023
'''
import tkinter

root = tkinter.Tk()

def get_key_data(event):
    char = event.char
    if char=='': char = event.keysym
    code = event.keycode
    print(char,code)
    #print(event.char,event.keysym,event.keycode,type(event.char))
def key_handler(event):
    print(end='+ ')
    get_key_data(event)
def key_handler_off(event):
    print(end='- ')
    get_key_data(event)

root.bind("<KeyPress>", key_handler)
root.bind("<KeyRelease>", key_handler_off)

root.mainloop()