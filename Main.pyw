from Batak import *

def main():
    window = Tk()
    window.geometry("800x600")
    window.title("Eşli Batak")
    window.iconphoto(True,PhotoImage(file="img/Logo.png"))
    window.config(background="#000000")
    window.resizable(height=False,width=False)
    titleImg = PhotoImage(file = "img/Title.png")
    title = Label(window,image = titleImg,borderwidth=0,highlightthickness=0,bg= "#000000")
    title.place(x = 57.5, y = 50)
    window.mainloop()

    #batak = Batak()

if __name__ == "__main__":
    main()