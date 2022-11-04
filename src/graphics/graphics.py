'''
This code write for project AVOCADO:
https://github.com/Ni3nayka/AVOCADO

Egor Bakay <egor_bakay@inbox.ru>
nov 2022
'''

try:
    from icon import add_my_icon_on_window
except ModuleNotFoundError:
    from graphics.icon import add_my_icon_on_window
    
from tkinter import *
from tkinter import messagebox
from time import sleep
from os import path
import webbrowser
import socket

class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder=None):
        super().__init__(master)

        if placeholder is not None:
            self.placeholder = placeholder
            self.placeholder_color = 'grey'
            self.default_fg_color = self['fg']

            self.bind("<FocusIn>", self.focus_in)
            self.bind("<FocusOut>", self.focus_out)

            self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()

class graphics:
    
    def __init__(self,title='AVOCADO graphics Debug',comanda_start=0,comanda_example=0):
        self.name = title
        self.window = Tk()
        self.window.title(self.name)
        add_my_icon_on_window(self.window)
        self.window.geometry('300x230')
        #self.window.resizable(0, 0)

        self.array_viget = []

        self.input_mode = ("gamepad")#,"console")
        self.contact_mode = ("wi-fi")#,"bluetooth","serial")

        self.input_mode_var = StringVar()
        self.contact_mode_var = StringVar()

        self.extern_fun = self.extern_fun_pass

        self.create_main_menu()

    def extern_fun_pass(self,command,data=""):
        print(command,data)

    def create_main_menu(self):

        lbl_ip = Label(text="ваш IP: " + str(socket.gethostbyname(socket.gethostname())))
        lbl_ip.place(relx=.5, rely=.7, anchor="c")
        self.array_viget.append(lbl_ip)
        
        lbl_1 = Label(text="Подключите геймпад")
        lbl_1.place(relx=.5, rely=.15, anchor="c")
        self.array_viget.append(lbl_1)

        # lbl_1 = Label(text="Выберите устройство ввода")
        # lbl_1.place(relx=.5, rely=.05, anchor="c")

        # input_mode_viget = ttk.Combobox(self.window, textvariable = self.input_mode_var)
        # input_mode_viget['values'] = self.input_mode
        # input_mode_viget['state'] = 'readonly'
        # input_mode_viget.place(relx=.5, rely=.15, anchor="c")
        # def callback_1(*arg):
        #     print(input_mode_viget.current(),self.input_mode_var.get())
        # self.input_mode_var.trace('w', callback_1)

        # lbl_2 = Label(text="Выберите метод усправления")
        # lbl_2.place(relx=.5, rely=.25, anchor="c")

        # contact_mode_viget = ttk.Combobox(self.window, textvariable = self.contact_mode_var)
        # contact_mode_viget['values'] = self.contact_mode
        # contact_mode_viget['state'] = 'readonly'
        # contact_mode_viget.place(relx=.5, rely=.35, anchor="c")
        # def callback_2(*arg):
        #     print(contact_mode_viget.current(),self.contact_mode_var.get())
        # self.contact_mode_var.trace('w', callback_2)

        # lbl_3 = Label(text="Запишите скорость обмена данными (Serial)")
        # lbl_3.place(relx=.5, rely=.45, anchor="c")

        # self.port_speed_viget = EntryWithPlaceholder(master=self.window,placeholder="9600")
        # self.port_speed_viget.place(relx=.5, rely=.55, anchor="c",height = 19,width = 150)

        lbl_4 = Label(text="Запишите порт (port)")
        lbl_4.place(relx=.5, rely=.35, anchor="c")
        self.array_viget.append(lbl_4)

        self.port_number_viget = EntryWithPlaceholder(master=self.window,placeholder="1234")
        self.port_number_viget.place(relx=.5, rely=.5, anchor="c",height = 19,width = 150)
        self.array_viget.append(self.port_number_viget)

        # link_button = Button(text="ссылка", command=self.open_link)
        # link_button.place(relx=.12, rely=.9, anchor="c",height = 40,width = 70)

        start_button = Button(text="старт",command=self.press_start) # , command=self.open_link
        start_button.place(relx=.5, rely=.9, anchor="c",height = 30,width = 70)
        self.array_viget.append(start_button)

    def create_gamepad_menu(self):
        end_button = Button(text="стоп",command=self.press_stop) # , command=self.open_link
        end_button.place(relx=.5, rely=.5, anchor="c",height = 30,width = 70)
        self.array_viget.append(end_button)

    def clear_viget(self):
        for a in self.array_viget:
            a.destroy()
        self.array_viget.clear()
    
    def press_start(self):
        try:
            try:
                #print(self.input_mode_var.get(),self.contact_mode_var.get(),self.port_number_viget.get())
                port = int(self.port_number_viget.get())
                if port<0 or port>99999:
                    messagebox.showerror("SaveSystem", "ERROR 3: порт не может иметь такой номер")
                    return
                self.extern_fun("start",port)
                self.clear_viget()
                self.create_gamepad_menu()
            except ValueError:
                messagebox.showerror("SaveSystem", "ERROR 2: порт не может быть не целочисленным")
        except AttributeError:
            messagebox.showerror("SaveSystem", "ERROR 1: ошибка вызова виджета с необходимыми данными")

    def press_stop(self):
        self.clear_viget()
        self.create_main_menu()
        self.extern_fun("stop")

        #messagebox.showerror("DevelopMessage", "Эта опция пока не реализоавна")

    def open_link(self):
        webbrowser.open('https://disk.yandex.ru/d/', new=2) # demo
        messagebox.showerror("SaveSystem", "по такому пути нет такого файла")
        #webbrowser.open('https://disk.yandex.ru/d/9bzTV6IxxkCIbw', new=2) # full
       
    def loop(self):
        self.window.mainloop()

if __name__=="__main__":
    # https://pythonguides.com/python-tkinter-button/    картинка в кнопке
    
    window = graphics()
    window.loop()
