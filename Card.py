from tkinter import *

class Card:
    value = None
    type = None
    img = None
    unplayable = None

    def __init__(self,value,type,path):
        self.value = value
        self.type = type
        self.img = PhotoImage(file=path)
        upath = "img/unplayable/" + path[4:] + ".png"
        self.unplayable = PhotoImage(file=upath)