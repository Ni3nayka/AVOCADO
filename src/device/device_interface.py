# все методы должны выполняться "мгновенно", а не "ожидать события"
# кроме метода init: он выполняется до момента подключения (или ошибки)
class device_pass:
    def __init__(self, *args): pass
    #def start(self, *args): pass
    def write(self, *args): pass
    def get(self, *args) -> str: return ""
    def test(self, *args) -> str: return "ok"
    def close(self, *args): pass