from Batak import *

window = Tk()
scores = None
language = None
mateRule = FALSE
nextGame = FALSE
starter = 0

def main():
    global language
    global scores
    global starter
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
    batak = Batak(language,mateRule,starter)
    starter = batak.getStarter()
    humanScores = []
    cpuScores = []
    while(TRUE):
        humanScores.append(batak.getScores()[0])
        cpuScores.append(batak.getScores()[1])
        if( language == 0): 
            title = "Scores"
            playertxt = "Player"
            cputxt = "Computer"
        else: 
            title = "Puanlar"
            playertxt = "Oyuncu"
            cputxt = "Bilgisayar"
        scores = Tk()
        scores.title(title)
        scores.iconphoto(True,PhotoImage(file="img/Logo.png"))
        scores.config(background="#000000")
        scores.resizable(height=False,width=False)
        playerText = Label(scores,text= playertxt,font=('Arial',20),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0,
                           width=10)
        cpuText = Label(scores,text= cputxt,font=('Arial',20),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0,
                           width=10)
        playerText.grid(row = 0,column=0)
        cpuText.grid(row = 0,column=1)
        for i in range(len(humanScores)):
            for j in range(2):
                color = ""
                if(j == 0):
                    txt = humanScores[i] 
                    if(humanScores[i] >= 0) : color = "#429bf5"
                    else : color = "#cf0a0a"
                else:
                    txt = cpuScores[i]
                    if(cpuScores[i] >= 0) : color = "#429bf5"
                    else : color = "#cf0a0a"   
                score = Label(scores,text= txt,font=('Arial',20),bg = "#000000",borderwidth=0,highlightthickness=0,
                             fg=color,width=10)
                score.grid(row=i+1,column=j)
        addImage = PhotoImage(file="img/addition.png")
        for i in range(2):
            addition = Label(scores,image= addImage,bg = "#000000",borderwidth=0,highlightthickness=0,)
            addition.grid(row = len(humanScores)+1,column = i)
            if ( i == 0) : txt = sum(humanScores)
            else : txt = sum(cpuScores)
            score = Label(scores,text= txt,font=('Arial',20),bg = "#000000",borderwidth=0,highlightthickness=0,
                             fg="#FFFFFF",width=10)
            score.grid(row = len(humanScores) + 2,column = i)
        if( language == 0) : msg = "Keep on playing"
        else : msg= "Oyuna devam"
        keepOnButton = Button(scores,command=keepOn,text=msg,font=('Arial',20),fg = "#FFFFFF",
                        bg= "#429bf5",borderwidth=0,highlightthickness=0)
        keepOnButton.grid(row = len(humanScores) + 3,column = 0)
        if( language == 0) : msg = "Quit the game ?"
        else : msg= "Oyundan çık"
        quitButton = Button(scores,command=quit,text=msg,font=('Arial',20),fg = "#FFFFFF",
                        bg= "#429bf5",borderwidth=0,highlightthickness=0)
        quitButton.grid(row = len(humanScores) + 3,column = 1)
        scores.mainloop()
        if(nextGame == TRUE):
            batak = Batak(language,mateRule,starter)
            starter = batak.getStarter()
        else : break


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

def keepOn():
    global nextGame
    global scores
    nextGame = TRUE
    scores.destroy()

def quit():
    global nextGame
    global scores
    nextGame = FALSE
    scores.destroy()
    

if __name__ == "__main__":
    main()

