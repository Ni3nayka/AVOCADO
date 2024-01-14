'''
Интерфейс для реализации подключения ко ВСЕМ устройствам (wifi,bluetooth,serial)

все методы должны выполняться "мгновенно", а не "ожидать события"
(нет) кроме метода init: он выполняется до момента подключения (или ошибки)
'''

class device_pass:
    # инициализация ВСЕГО необходимого
    def __init__(self, a=False, *args): 
        if not a: basic_warning()
        self.DEVICE_SETUP = "setup" # константа - девайс запускается
        self.DEVICE_OK = "ok" # константа - девайс запущен
    # отправить девайсу строку
    def write(self, line, *args): 
        basic_warning()
    # получить с девайса строку (если пришла)
    def get(self, *args) -> str: 
        basic_warning()
        return ""
    # получить состояние соединения с устройством
    def test(self, *args) -> str: 
        basic_warning()
        return "ok" # "setup"-идет инициализация, "ok"-все работает, остальное - соединение завершено по той или иной причине 
    # закрыть соединение с устройством
    def close(self, *args): 
        basic_warning()

def basic_warning(): # сообщать что используется интерфейс а не наследующий его класс
    print("WARNING: use basic device interface!")