from src.Game import *

class StartingScreen:
    def __init__(self):
        self.window = Tk()
        self.scores = None
        self.language = None
        self.mateRule = FALSE
        self.nextGame = TRUE
        self.starter = 0
        self.window.geometry("800x600")
        self.window.title("Eşli Batak")
        self.window.iconphoto(True,PhotoImage(file="img/Logo.png"))
        self.window.config(background="#000000")
        self.window.resizable(height=False,width=False)
        titleImg = PhotoImage(file = "img/Title.png")
        title = Label(self.window,image = titleImg,borderwidth=0,highlightthickness=0,bg= "#000000")
        title.place(x = 57.5, y = 50)
        turkBayragi = PhotoImage(file = "img/TurkBayragi.png")
        unionJack = PhotoImage(file = "img/UnionJack.png")
        turkish = Button(self.window,command=self.turkishButton,image=turkBayragi,borderwidth=0,highlightthickness=0)
        english = button = Button(self.window,command=self.englishButton,image=unionJack,borderwidth=0,highlightthickness=0)
        turkish.place( x=150,y=275)
        english.place( x=450,y=275)
        textTurkish = Label(self.window,text= "Türkçe",font=('Arial',35),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0)
        textEnglish = Label(self.window,text= "English",font=('Arial',35),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0)
        textTurkish.place( x=175,y=200)
        textEnglish .place( x=470,y=200)
        self.window.mainloop()
        humanScores = []
        cpuScores = []
        while(TRUE):
            if(self.nextGame == TRUE):
                game = Game(self.language,self.mateRule,self.starter)
                self.starter = game.getStarter()
            else : break
            if(game.closed == FALSE):
                humanScores.append(game.getScores()[0])
                cpuScores.append(game.getScores()[1])
            if( self.language == 0): 
                title = "Scores"
                playertxt = "Player"
                cputxt = "Computer"
            else: 
                title = "Puanlar"
                playertxt = "Oyuncu"
                cputxt = "Bilgisayar"
            self.scores = Tk()
            self.scores.title(title)
            self.scores.iconphoto(True,PhotoImage(file="img/Logo.png"))
            self.scores.config(background="#000000")
            self.scores.resizable(height=False,width=False)
            playerText = Label(self.scores,text= playertxt,font=('Arial',20),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0,
                            width=10)
            cpuText = Label(self.scores,text= cputxt,font=('Arial',20),fg="#FFFFFF",bg = "#000000",borderwidth=0,highlightthickness=0,
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
                    score = Label(self.scores,text= txt,font=('Arial',20),bg = "#000000",borderwidth=0,highlightthickness=0,
                                fg=color,width=10)
                    score.grid(row=i+1,column=j)
            addImage = PhotoImage(file="img/addition.png")
            for i in range(2):
                addition = Label(self.scores,image= addImage,bg = "#000000",borderwidth=0,highlightthickness=0,)
                addition.grid(row = len(humanScores)+1,column = i)
                if ( i == 0) : txt = sum(humanScores)
                else : txt = sum(cpuScores)
                score = Label(self.scores,text= txt,font=('Arial',20),bg = "#000000",borderwidth=0,highlightthickness=0,
                                fg="#FFFFFF",width=10)
                score.grid(row = len(humanScores) + 2,column = i)
            if( self.language == 0) : msg = "Keep on playing"
            else : msg= "Oyuna devam"
            keepOnButton = Button(self.scores,command=self.keepOn,text=msg,font=('Arial',20),fg = "#FFFFFF",
                            bg= "#429bf5",borderwidth=0,highlightthickness=0)
            keepOnButton.grid(row = len(humanScores) + 3,column = 0)
            if( self.language == 0) : msg = "Quit the game ?"
            else : msg= "Oyundan çık"
            quitButton = Button(self.scores,command=self.quit,text=msg,font=('Arial',20),fg = "#FFFFFF",
                            bg= "#429bf5",borderwidth=0,highlightthickness=0)
            quitButton.grid(row = len(humanScores) + 3,column = 1)
            self.scores.mainloop()
    
    def fMateRule(self):
        msg = ""
        if(self.language == 1) : msg = "Bilgisayar eşiniz olarak ihaleye girsin mi ?"
        else : msg = "Do you want the computer\n     to bid as your mate ?"
        self.mateRule = FALSE
        if messagebox.askyesno(title='Eşli Batak',message=msg): mateRule = TRUE

    def turkishButton(self): 
        self.language = 1
        self.fMateRule()
        self.window.destroy()

    def englishButton(self): 
        self.language = 0
        self.fMateRule()
        self.window.destroy()

    def keepOn(self):
        self.nextGame = TRUE
        self.scores.destroy()

    def quit(self):
        self.nextGame = FALSE
        self.scores.destroy()