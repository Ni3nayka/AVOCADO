from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
 
 
class Example(Frame):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.master.title("Кнопки в kinter")
        self.style = Style()
        self.style.theme_use("default")
 
        #frame = Frame(self, relief=RAISED, borderwidth=1)
        #frame.pack(fill=BOTH, expand=True)
 
        self.pack(fill=BOTH, expand=True)
 
        closeButton = Button(text="Закрыть")
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        okButton = Button(text="Готово")
        okButton.pack(side=RIGHT)
 
 
def main():
 
    root = Tk()
    root.geometry("300x200+300+300")
    app = Example()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()