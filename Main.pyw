from Batak import *

window = Tk()
language = None

def main():
    
    window.geometry("800x600")
    window.title("Eşli Batak")
    window.iconphoto(True,PhotoImage(file="img/Logo.png"))
    window.config(background="#000000")
    window.resizable(height=False,width=False)
    titleImg = PhotoImage(file = "img/Title.png")
    title = Label(window,image = titleImg,borderwidth=0,highlightthickness=0,bg= "#000000")
    title.place(x = 57.5, y = 50)
    turkBayragi = PhotoImage(file = "img/TurkBayragi.png")
    unionJack = PhotoImage(file = "img/UnionJack.png")
    turkish = Button(window,command=turkishButton,image=turkBayragi,borderwidth=0,highlightthickness=0)
    english = button = Button(window,command=englishButton,image=unionJack,borderwidth=0,highlightthickness=0)
    turkish.place( x=150,y=350)
    english.place( x=450,y=350)
    textTurkish = Label(window,text= "Türkçe",font=('Arial',35),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0)
    textEnglish = Label(window,text= "English",font=('Arial',35),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0)
    textTurkish.place( x=175,y=275)
    textEnglish .place( x=470,y=275)
    window.mainloop()
    batak = Batak(language)

def turkishButton(): 
    global language
    global window
    language = 1
    window.destroy()

def englishButton(): 
    global language
    global window
    language = 0
    window.destroy()

if __name__ == "__main__":
    main()