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
from tkinter import ttk
from time import sleep
from os import path
import webbrowser
import socket

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
    
    def __init__(self,title='AVOCADO graphics Debug'):
        self.name = title
        self.window = Tk()
        self.window.title(self.name)
        add_my_icon_on_window(self.window)
        #self.window.geometry('360x200')
        #self.window.resizable(0, 0)

        self.array_viget = []
        self.text_monitor_viget = 0

        self.input_mode = ("геймпад","консоль","геймпад и консоль")
        self.contact_mode = ("wi-fi","bluetooth") # ,"serial"

        self.input_mode_var = StringVar()
        self.contact_mode_var = StringVar()
        self.ip_port = 1234
        self.autoscroll_monitor_viget = True

        self.extern_fun = self.extern_fun_pass

        self.create_main_menu()

        # UP MENU
        self.MENU = Menu(self.window) 

        self.new_item_m = Menu(self.MENU)  
        self.new_item_m.add_command(label='мануал по использованию программы',command=lambda:webbrowser.open('https://docs.google.com/document/d/1Rvoi-yDUz9T8iqtriVZaRBL97akOxsfKGw68NE6AFoM/edit?usp=share_link', new=2)) 
        self.new_item_m.add_separator()
        self.new_item_m.add_command(label='скачать Arduino IDE',command=lambda:webbrowser.open('https://www.arduino.cc/en/software', new=2))  
        self.new_item_m.add_command(label='установить esp в Arduino IDE (1)',command=lambda:webbrowser.open('https://radioprog.ru/post/863', new=2)) 
        self.new_item_m.add_command(label='установить esp в Arduino IDE (2)',command=lambda:webbrowser.open('https://alexgyver.ru/lessons/esp8266/', new=2)) 
        self.new_item_m.add_command(label='мануал для прошивки по wifi',command=lambda:webbrowser.open('https://habr.com/ru/company/first/blog/654623/', new=2)) 
        self.MENU.add_cascade(label='мануал', menu=self.new_item_m)

        self.new_item_i = Menu(self.MENU)  
        self.new_item_i.add_command(label='новую версию программы',command=lambda:webbrowser.open('https://github.com/Ni3nayka/AVOCADO/releases', new=2))
        self.new_item_i.add_command(label='библиотеку для esp',command=lambda:webbrowser.open('https://github.com/Ni3nayka/AVOCADO_esp/releases', new=2))
        self.MENU.add_cascade(label='скачать', menu=self.new_item_i)

        self.new_item_11 = Menu(self.MENU)  
        self.new_item_11.add_command(label='оценить',command=lambda:webbrowser.open('https://forms.gle/N7n5erFaajJRRawG6', new=2)) 
        self.new_item_11.add_command(label='о программе',command=self.about_program) 
        self.MENU.add_cascade(label='о программе', menu=self.new_item_11)

        self.window.config(menu=self.MENU)

        self.expectation_viget = Label(text="Ожидание подключения....")

    def create_expectation_viget(self):
        self.del_expectation_viget()
        self.expectation_viget = Label(text="Ожидание подключения....")
        self.expectation_viget.place(relx=.5, rely=.15, anchor="c")

    def del_expectation_viget(self):
        try: self.expectation_viget.destroy()
        except RuntimeError: print("параша потоков")

    def develop_message(self):
        messagebox.showerror("SaveSystem", "к сожалению данная опция пока в разработке")

    def about_program(self):
        messagebox.showinfo("о программе", "Проект AVOCADO состоит из библиотек для разных микроконтроллеров (ESP и Arduino) и программы под windows для управления этими контроллерами с помощью библиотек при использовании минимума кода.\nАвтор: Бакай Егор\negor_bakay@inbox.ru\nг.Москва 2022 г.")

    def extern_fun_pass(self,command,data=""):
        print(command,data)

    def create_main_menu(self):
        self.window.geometry('360x200')

        lbl_ip = Label(text="ваш IP: " + str(get_ip()))
        lbl_ip.place(relx=.5, rely=.55, anchor="c")
        self.array_viget.append(lbl_ip)

        lbl_1 = Label(text="Выберите управляющее устройство")
        lbl_1.place(relx=.29, rely=.15, anchor="c")
        self.array_viget.append(lbl_1)

        input_mode_viget = ttk.Combobox(self.window, textvariable = self.input_mode_var)
        input_mode_viget['values'] = self.input_mode
        input_mode_viget['state'] = 'readonly'
        try: input_mode_viget.set(self.input_mode[list(self.input_mode).index(self.input_mode_var.get())])
        except ValueError: input_mode_viget.set(self.input_mode[0])
        input_mode_viget.place(relx=.78, rely=.15, anchor="c")
        # def callback_1(*arg):
        #     #print(input_mode_viget.current(),self.input_mode_var.get())
        #     print(self.input_mode_var.get())
        # self.input_mode_var.trace('w', callback_1)
        self.array_viget.append(input_mode_viget)

        lbl_2 = Label(text="Выберите способ передачи данных")
        lbl_2.place(relx=.29, rely=.35, anchor="c")
        self.array_viget.append(lbl_2)

        contact_mode_viget = ttk.Combobox(self.window, textvariable = self.contact_mode_var)
        contact_mode_viget['values'] = self.contact_mode
        contact_mode_viget['state'] = 'readonly'
        try: contact_mode_viget.set(self.contact_mode[list(self.contact_mode).index(self.contact_mode_var.get())])
        except ValueError: contact_mode_viget.set(self.contact_mode[0])
        contact_mode_viget.place(relx=.78, rely=.35, anchor="c")
        self.array_viget.append(contact_mode_viget)

        # self.port_speed_viget = EntryWithPlaceholder(master=self.window,placeholder="9600")
        # self.port_speed_viget.place(relx=.5, rely=.55, anchor="c",height = 19,width = 150)

        lbl_4 = Label(text="Запишите номер порта")
        lbl_4.place(relx=.36, rely=.7, anchor="c")
        self.array_viget.append(lbl_4)

        self.port_number_viget = EntryWithPlaceholder(master=self.window,placeholder=str(self.ip_port))
        self.port_number_viget.place(relx=.7, rely=.7, anchor="c",height = 19,width = 100)
        self.array_viget.append(self.port_number_viget)

        start_button = Button(text="старт",command=self.press_start)
        start_button.place(relx=.5, rely=.9, anchor="c",height = 30,width = 70) 
        self.array_viget.append(start_button)

    def create_monitor_menu(self):
        self.window.geometry('700x300')

        # https://metanit.com/python/tkinter/2.4.php

        # фрейм для нижних объектов
        frame = Frame()
        frame.pack(fill=X,side=BOTTOM)
        self.array_viget.append(frame)

        # кнопка выйти
        end_button = Button(frame,text="выйти",command=self.press_stop) 
        end_button.pack(side=LEFT, ipadx=2, ipady=2, padx=3, pady=3)
        self.array_viget.append(end_button)

        # кнопка для отправки сообщения из виджета для ввода
        def send_wifi_message(a=0): # a - переменная нужна для работы bind при нажатии кнопки enter (просто он отправляет данные, надо как-то принять)
            self.extern_fun("monitor_message",entry.get())
            #self.add_line_to_text_monitor_viget(entry.get()) # test
            entry.delete(0, END)   # удаление введенного текста
        send_button = Button(frame,text="отправить",command=send_wifi_message) 
        send_button.pack(side=RIGHT, ipadx=2, ipady=2, padx=3, pady=3) 
        self.array_viget.append(send_button)

        # кнопка для очистки поля вывода
        def clear_viget():
            self.text_monitor_viget.configure(state=NORMAL)
            self.text_monitor_viget.delete(1.0, END) 
            self.text_monitor_viget.configure(state=DISABLED)
        clear_button = Button(frame,text="очистить",command=clear_viget) 
        clear_button.pack(side=LEFT, ipadx=2, ipady=2, padx=3, pady=3) 
        self.array_viget.append(clear_button)

        # кнопка для сключения или выключения автопрокрутки
        btn_text = StringVar(value="автопрокрутка - on")
        self.autoscroll_monitor_viget = True
        def update_btn_text():
            self.autoscroll_monitor_viget = not self.autoscroll_monitor_viget
            btn_text.set("автопрокрутка - on" if self.autoscroll_monitor_viget else "автопрокрутка - off")
        btn_autoscroll = Button(frame,textvariable=btn_text, command=update_btn_text)
        btn_autoscroll.pack(side=LEFT, ipadx=2, ipady=2, padx=3, pady=3) 
        self.array_viget.append(btn_autoscroll)

        # поле (снизу) для ввода пользовательского текста
        entry = ttk.Entry(frame)
        entry.pack(side=BOTTOM, fill=X, pady=5, ipady=2) # , padx=6, pady=6
        entry.bind('<Return>', send_wifi_message)
        self.array_viget.append(entry)

        # большое поле для вывода полученной инфы
        self.text_monitor_viget = Text(state='disabled')
        scroll = Scrollbar(command=self.text_monitor_viget.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.text_monitor_viget.pack(side=RIGHT,fill=BOTH,padx=2, expand=True)
        self.text_monitor_viget.config(yscrollcommand=scroll.set)
        self.array_viget.append(self.text_monitor_viget)
        self.array_viget.append(scroll)

        self.create_expectation_viget()

    def add_line_to_text_monitor_viget(self,line):
        try: 
            self.text_monitor_viget.configure(state=NORMAL)
            self.text_monitor_viget.insert(END, line) # +"\n" 
            if self.autoscroll_monitor_viget:
                self.text_monitor_viget.see(END)
            self.text_monitor_viget.configure(state=DISABLED)
        except AttributeError: pass

    def create_gamepad_menu(self):
        end_button = Button(text="стоп",command=self.press_stop) 
        end_button.place(relx=.5, rely=.5, anchor="c",height = 30,width = 70)
        self.array_viget.append(end_button)

        self.create_expectation_viget()

    def clear_viget(self):
        for a in self.array_viget:
            a.destroy()
        self.array_viget.clear()
    
    def press_start(self):
        try:
            # port
            if self.contact_mode_var.get()=="wi-fi": # self.input_mode_var.get()=="геймпад":
                try:
                    port = int(self.port_number_viget.get())
                except ValueError:
                    messagebox.showerror("SaveSystem", "ERROR 2: порт не может быть не целочисленным (пример: 1234)")
                    return
                if port<0 or port>99999:
                    messagebox.showerror("SaveSystem", "ERROR 3: порт не может иметь такой номер (пример: 1234)")
                    return
                self.ip_port = port
            elif self.contact_mode_var.get()=="bluetooth":
                # while dont work
                messagebox.showerror("SaveSystem", "Извините, блютуз пока не работает, доделаю в следующей версии :)")
                return
                #
                port = self.port_number_viget.get()
                if len(port.split(":"))!=6:
                    messagebox.showerror("SaveSystem", "ERROR 6: порт не может иметь такой номер (пример: 20:A6:B6:23:0C:27)")
                    return
                self.ip_port = port
            elif self.contact_mode_var.get()=="":
                messagebox.showinfo("SaveSystem", "Выберите способ передачи данных")
                return
            else:
                messagebox.showerror("SaveSystem", "ERROR 5: неизвестный режим передачи данных")
                return
            # graphic - device
            commanda = "start"
            if self.input_mode_var.get().find("геймпад")!=-1:
                commanda += "_gamepad"
                self.clear_viget()
                self.create_gamepad_menu()
            if self.input_mode_var.get().find("консоль")!=-1:
                commanda += "_monitor"
                self.clear_viget()
                self.create_monitor_menu()
            if commanda=="start":
                messagebox.showinfo("SaveSystem", "Выберите управляющее устройство")
                return
            self.extern_fun(commanda,port)
        except AttributeError:
            messagebox.showerror("SaveSystem", "ERROR 1: ошибка вызова виджета с необходимыми данными")

    def press_stop(self):
        self.clear_viget()
        self.create_main_menu()
        self.extern_fun("stop")
       
    def loop(self):
        self.window.mainloop()

if __name__=="__main__":
    # https://pythonguides.com/python-tkinter-button/    картинка в кнопке
    
    window = graphics()
    window.loop()
