from tkinter import *
from tkinter import ttk

# Создайте экземпляр фрейма или окна tkinter
window = Tk()

# Установить размер окна
window.geometry("700x350")

# Создайте функцию для очистки поля со списком
def clear_combobox():
  combobox.set('')

# Определить кортеж дней
days = ('Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье')

# Функция для печати индекса выбранной опции в Combobox
def callback(*arg):
  Label(window, text = 'Индекс равен' + str(combobox.current()) + ' для ' + ' ' + str(var.get()), font = ('Helvetica 12') ).pack()


# Создайте виджет со списком
var = StringVar()
combobox = ttk.Combobox(window, textvariable = var)
combobox['values'] = days
combobox['state'] = 'readonly'
combobox.pack(fill='x',padx= 5, pady=5)

# Установите трассировку для данной переменной
var.trace('w', callback)


# Создайте кнопку, чтобы очистить выбранное текстовое значение поля со списком
button = Button(window, text = 'очистить', command = clear_combobox)
button.pack()


window.mainloop()