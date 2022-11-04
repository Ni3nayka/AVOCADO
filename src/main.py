from graphics.graphics import graphics,messagebox


def test(command,data=""):
    print(command,data)
    messagebox.showinfo("SaveSystem", "WARNING: Геймпад или не подключен или работает некорректно")

window = graphics()
window.extern_fun = test
window.loop()