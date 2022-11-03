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
from tkinter import ttk
from tkinter import messagebox
from time import sleep
from os import path
import webbrowser

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

        self.input_mode = ("gamepad","console")
        self.contact_mode = ("wi-fi","bluetooth","serial")

        # Функция для печати индекса выбранной опции в Combobox

        lbl_1 = Label(text="Выберите устройство ввода")
        lbl_1.place(relx=.5, rely=.05, anchor="c")

        self.input_mode_var = StringVar()
        self.input_mode_viget = ttk.Combobox(self.window, textvariable = self.input_mode_var)
        self.input_mode_viget['values'] = self.input_mode
        self.input_mode_viget['state'] = 'readonly'
        self.input_mode_viget.place(relx=.5, rely=.15, anchor="c")
        def callback_1(*arg):
            print(self.input_mode_viget.current(),self.input_mode_var.get())
        self.input_mode_var.trace('w', callback_1)

        lbl_2 = Label(text="Выберите метод усправления")
        lbl_2.place(relx=.5, rely=.25, anchor="c")

        self.contact_mode_var = StringVar()
        self.contact_mode_viget = ttk.Combobox(self.window, textvariable = self.contact_mode_var)
        self.contact_mode_viget['values'] = self.contact_mode
        self.contact_mode_viget['state'] = 'readonly'
        self.contact_mode_viget.place(relx=.5, rely=.35, anchor="c")
        def callback_2(*arg):
            print(self.contact_mode_viget.current(),self.contact_mode_var.get())
        self.contact_mode_var.trace('w', callback_2)

        lbl_3 = Label(text="Запишите скорость обмена данными (Serial)")
        lbl_3.place(relx=.5, rely=.45, anchor="c")

        self.port_speed_viget = EntryWithPlaceholder(master=self.window,placeholder="9600")
        self.port_speed_viget.place(relx=.5, rely=.55, anchor="c",height = 19,width = 150)

        lbl_4 = Label(text="Запишите порт (Serial, bluetooth)")
        lbl_4.place(relx=.5, rely=.65, anchor="c")

        self.port_number_viget = EntryWithPlaceholder(master=self.window,placeholder="COM1")
        self.port_number_viget.place(relx=.5, rely=.75, anchor="c",height = 19,width = 150)

        # link_button = Button(text="ссылка", command=self.open_link)
        # link_button.place(relx=.12, rely=.9, anchor="c",height = 40,width = 70)

        start_button = Button(text="старт") # , command=self.open_link
        start_button.place(relx=.5, rely=.9, anchor="c",height = 30,width = 70)

        # self.file_path = ""
        # self.comanda_start = comanda_start
        # if self.comanda_start==0: self.comanda_start = self.plug
        # self.comanda_example = comanda_example
        # if self.comanda_example==0: self.comanda_example = self.plug

        # # self.file_path = StringVar()
        # # self.message_entry = Entry(textvariable=self.file_path)
        # # self.message_entry.place(relx=.4, rely=.1, anchor="c")

        # self.lbl_file = Label(text="")
        # self.lbl_file.place(relx=.5, rely=.1, anchor="c")

        # self.lbl = Label(text="выберите файл и запишите необходимые данные")
        # self.lbl.place(relx=.5, rely=.2, anchor="c")
        
        # link_button = Button(text="ссылка", command=self.open_link)
        # link_button.place(relx=.12, rely=.9, anchor="c",height = 40,width = 70)

        # example_button = Button(text="пример", command=self.add_example)
        # example_button.place(relx=.37, rely=.9, anchor="c",height = 40,width = 70)

        # file_button = Button(text="обзор", command=self.test_file_path)
        # file_button.place(relx=.62, rely=.9, anchor="c",height = 40,width = 70)

        # start_button = Button(text="старт", command=self.start_operating)
        # start_button.place(relx=.87, rely=.9, anchor="c",height = 40,width = 70)

        # self.message_sport_category = EntryWithPlaceholder(master=self.window,placeholder="столбец разрядов (A..ZZZ)")
        # self.message_sport_category.place(relx=.5, rely=.3, anchor="c",height = 19,width = 280)
        # self.message_start_rez = EntryWithPlaceholder(master=self.window,placeholder="первый столбец результатов (A..ZZZ)")
        # self.message_start_rez.place(relx=.5, rely=.39, anchor="c",height = 19,width = 280)
        # self.message_end_rez = EntryWithPlaceholder(master=self.window,placeholder="последний столбец результатов (A..ZZZ)")
        # self.message_end_rez.place(relx=.5, rely=.48, anchor="c",height = 19,width = 280)
        # self.message_start_line = EntryWithPlaceholder(master=self.window,placeholder="первая строка результатов (1..999)")
        # self.message_start_line.place(relx=.5, rely=.57, anchor="c",height = 19,width = 280)
        # self.message_end_line = EntryWithPlaceholder(master=self.window,placeholder="последняя строка результатов (1..999)")
        # self.message_end_line.place(relx=.5, rely=.66, anchor="c",height = 19,width = 280)
        # self.message_rang = EntryWithPlaceholder(master=self.window,placeholder="столбец получаемых разрядов (A..ZZZ)")
        # self.message_rang.place(relx=.5, rely=.75, anchor="c",height = 19,width = 280)
                
    def open_link(self):
        webbrowser.open('https://disk.yandex.ru/d/R5s-2UDF0x7j5Q', new=2) # demo
        #webbrowser.open('https://disk.yandex.ru/d/9bzTV6IxxkCIbw', new=2) # full

    def test_file_path(self):
        self.file_path = "dfsgg"#file_choice()
        self.lbl_file.config(text=self.file_path)
        self.lbl.config(text="нажмите старт")
        #self.message_entry.config(text=self.file_path)

    def add_example(self):
        self.comanda_example()
        self.lbl.config(text="пример создан")

    def start_operating(self):
        
        def test(A):
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            B = A.get().upper()
            if B=="": return True
            for a in B:
                try: alphabet.index(a)
                except ValueError: return True
            return False

        if test(self.message_sport_category):
            messagebox.showerror("SaveSystem", "столбец разрядов (1) введен неверно")
            return
        if test(self.message_start_rez):
            messagebox.showerror("SaveSystem", "первый столбец результатов (2) введен неверно")
            return
        if test(self.message_end_rez):
            messagebox.showerror("SaveSystem", "последний столбец результатов (3) введен неверно")
            return
        if not self.message_start_line.get().isdigit(): 
            messagebox.showerror("SaveSystem", "первая строка результатов (4) введена неверно")
            return
        if not self.message_end_line.get().isdigit(): 
            messagebox.showerror("SaveSystem", "последняя строка результатов (5) введена неверно")
            return
        if test(self.message_rang): 
            messagebox.showerror("SaveSystem", "столбец получаемых разрядов (5) введен неверно")
            return
        if not path.exists(self.file_path):
            messagebox.showerror("SaveSystem", "по такому пути нет такого файла")
            return
             
        self.lbl.config(text="файл обрабатывается.....")
        self.window.update()
        self.comanda_start(self.file_path)
        #sleep(0.5)
        self.lbl.config(text="файл обрабобтан")
        #print(self.file_path)

    def loop(self):
        self.window.mainloop()

    def plug(self,*arg): # pass
        print(self.get_data())

    def get_data(self):
        return [self.message_sport_category.get(),self.message_start_rez.get(),self.message_end_rez.get(),int(self.message_start_line.get()),int(self.message_end_line.get())],[int(self.message_start_line.get()),self.message_rang.get()]
        
        
    

if __name__=="__main__":
    # https://pythonguides.com/python-tkinter-button/    картинка в кнопке
    
    window = graphics()
    window.loop()
