'''
link:
https://www.youtube.com/watch?v=CKSd9A88qvM
https://github.com/NetroScript/Graveyard-Keeper-Savefile-Editor/issues/43

This code write for project box_distributor:
https://github.com/Ni3nayka/box_distributor

Egor Bakay <egor_bakay@inbox.ru>
may 2022
'''

import os
from tkinter import *
import base64
from io import BytesIO
from PIL import Image, ImageTk

# if this line have error, recompiling ico
try: from icon_img import IMAGE
except ModuleNotFoundError: 
    try: from graphics.icon_img import IMAGE
    except ModuleNotFoundError: print("WARNING: no file <icon_img.py>")

def creare_new_icon_on_window(pict): # for create code from ico image
    #pict = 'D:/GitHub/box_distributor/src/graphics/ava.ico'
    try:
        with open(pict, 'rb') as f:
            binary = base64.b64encode(f.read())
    except FileNotFoundError:
        pict = str(os.path.dirname(os.path.abspath(__file__))) + "/" + pict
        with open(pict, 'rb') as f:
            binary = base64.b64encode(f.read())
    file = open(str(os.path.dirname(os.path.abspath(__file__)))+"/icon_img.py", 'w')
    file.write("# This file is created automatically to store the application icon as text\n")
    file.write("# link project: https://github.com/Ni3nayka/box_distributor\n")
    file.write("# Egor Bakay <egor_bakay@inbox.ru>\n")
    file.write("\nIMAGE = ")
    file.write(str(binary))
    file.write("\n\n")
    file.close()
    

def add_my_icon_on_window(window):

    # translate code to icon window
    image = BytesIO(base64.b64decode(IMAGE))
    pillow = Image.open(image)
    pillow2 = ImageTk.PhotoImage(pillow)
    
    window.iconphoto(True, pillow2)

if __name__=="__main__":

    if 1:
        # test icon
        window = Tk()  
        window.title("test ico")  
        window.geometry('600x450')
        
        add_my_icon_on_window(window)
        
        window.mainloop()
    else:
        # create icon
        creare_new_icon_on_window('ava.ico')
