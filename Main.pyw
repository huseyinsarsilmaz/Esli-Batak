from Batak import *

window = Tk()
language = None
mateRule = FALSE

def main():
    global language
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
    turkish.place( x=150,y=275)
    english.place( x=450,y=275)
    textTurkish = Label(window,text= "Türkçe",font=('Arial',35),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0)
    textEnglish = Label(window,text= "English",font=('Arial',35),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0)
    textTurkish.place( x=175,y=200)
    textEnglish .place( x=470,y=200)
    window.mainloop()
    batak = Batak(language,mateRule,0)
    while(TRUE):
        starter = batak.bidStarter()
        batak = Batak(language,mateRule,starter)
    

def fMateRule():
    global mateRule
    msg = ""
    if(language == 1) : msg = "Bilgisayar eşiniz olarak ihaleye girsin mi ?"
    else : msg = "Do you want the computer\n     to bid as your mate ?"
    mateRule = FALSE
    if messagebox.askyesno(title='Eşli Batak',message=msg): mateRule = TRUE

def turkishButton(): 
    global language
    global window
    language = 1
    fMateRule()
    window.destroy()

def englishButton(): 
    global language
    global window
    language = 0
    fMateRule()
    window.destroy()

if __name__ == "__main__":
    main()

