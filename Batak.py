from tkinter import *
from tkinter import messagebox
import time
import random

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

class Batak:
    def __init__(self,language,mateRule,starter):
        self.window = Tk()
        self.mateRule = mateRule 
        self.cards = []
        self.labels = []
        self.cardBackV = None
        self.cardBackH = None
        self.score = None
        self.inputs = []
        self.trump = None
        self.radio = IntVar()
        self.images = []
        self.positions = []
        self.playedCards = []
        self.greatest = None
        self.playedLabels = []
        self.turn = None
        self.turnType = None
        self.oldType = None
        self.winner = None
        self.humanScore = None
        self.cpuScore = None
        self.starter = starter
        self.bidder = starter
        self.bidwinner = starter
        self.bid = 6
        self.bidTurn = 0
        self.cpuTrump = ""
        self.activeCards = []    
        self.language = language
        self.closed = FALSE
        self.texts = [ ["Your bid ?","Trump ?","Player","Computer"] , ["  İhale ?","  Koz ?","Oyuncu","Bilgisayar"]]
        self.loadImages()
        self.createWindow()
        self.createCards()
        self.sortCards()
        self.createLabels()
        self.biddingStage()
        self.window.mainloop()

    def loadImages(self):
        for i in range(52) : self.activeCards.append(FALSE)
        self.cardBackV =PhotoImage(file = "img/back_v.png") ; self.cardBackH =PhotoImage(file = "img/back.png")
        self.score = PhotoImage(file = "img/score.png")
        Suits = [PhotoImage(file = "img/Logo.png"),PhotoImage(file = "img/Club.png"),PhotoImage(file = "img/Diamond.png"),
                PhotoImage(file = "img/Heart.png")]
        for i in range(4) : self.images.append(Suits[i])

    def onClose(self):
        self.closed = TRUE
        self.window.destroy()
    
    def createWindow(self):
        self.window.geometry("1400x800")
        self.window.title("Eşli Batak")
        self.window.iconphoto(True,PhotoImage(file="img/Logo.png"))
        self.window.config(background="#096b1b")
        self.window.resizable(height=False,width=False)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

    def createCards(self):
        types = ["clubs","diamonds","spades","hearts"]
        Values = ["jack","queen","king","ace"]
        for i in range(4):
            for j in range(2,15):
                path  = "img/"
                if(j<11): path += str(j)
                else : path += Values[j-11]
                path += "_of_" + types[i] + ".png"
                self.cards.append(Card(j,types[i],path))
        random.shuffle(self.cards)
        
    def sortCards(self):
        newCards = []
        types = ["diamonds","spades","hearts","clubs"]
        spades = [] ; hearts = [] ; diamonds = [] ; clubs = []    
        suits = [diamonds,spades,hearts,clubs]
        for i in range(4):
            for j in range(13):
                card = self.cards[ (13*i) + j ]
                for k in range(4) : 
                    if(card.type == types[k]) :suits[k].append(card)
            for j in range (4) : suits[j].sort(key= lambda item : item.value)
            for j in range(4):
                for k in range(len(suits[j])):
                    newCards.append(suits[j][k])
            for j in range(4) : suits[j].clear()
        self.cards = newCards
    
    def biddingStage(self):
        if ( self.bidTurn < 4):
            if( self.bidder == 0):
                first = FALSE
                if( self.bidder == self.starter) : first = TRUE
                self.Settings(first)
            elif( self.bidder == 1):
                if( self.mateRule == TRUE) : self.cpuBid(self.bidder)
                else: self.passTurn()
            else : self.cpuBid(self.bidder)
        elif(self.bidTurn == 4):
            for i in range(13,26) : self.labels[i].config(image=self.cards[i].img)
            humanText = Label(self.window,text= self.texts[self.language][2],
                              font=('Arial',30),fg='#FFFFFF',bg='#096b1b',height=1,width=8)
            humanText.place(x = 40,y=20)
            cpuText = Label(self.window,text= self.texts[self.language][3],
                            font=('Arial',30),fg='#FFFFFF',bg='#096b1b',height=1,width=10)
            cpuText.place(x = 1140,y=20)
            self.turnType = "Beginning"
            self.turn = 0 ; self.humanScore = 0 ; self.cpuScore = 0
            self.bidTurn = 99
            if( self.bidwinner == 0):
                for i in range(13):
                    self.labels[i].bind("<Enter>",self.cardSelect)
                    self.labels[i].bind("<Leave>",self.cardDeselect)
                    self.labels[i].bind("<Button-1>",self.humanPlay)
            else:
                self.trump = self.cpuTrump
                print(self.trump)
                types = ["spades","clubs","diamonds","hearts"]
                if ( self.language == 0) : msg = "Trump: "
                else: msg = "Koz:  "
                trumpText = Label(self.window,text=msg,font=('Arial',45),fg='#FFFFFF',bg='#096b1b',)
                trumpImage = Label(self.window,image=self.images[types.index(self.trump)])
                trumpText.place(x = 562 , y= 342)
                trumpImage.place(x = 800 , y=352)
                self.window.update()
                time.sleep(3)
                trumpText.destroy()
                trumpImage.destroy()
                self.window.update()
                if( self.bidwinner == 1):
                    for i in range(13,26):
                        self.labels[i].bind("<Enter>",self.cardSelect)
                        self.labels[i].bind("<Leave>",self.cardDeselect)
                        self.labels[i].bind("<Button-1>",self.humanPlay)
                elif( self.bidwinner == 2) : self.cpuplay(3,0)  
                else : self.cpuplay(4,1)                    
    
    def Settings(self,isFirst):
        self.inputs.append(Scale(self.window,from_=self.bid+1,to=13,length=220,font = ('Consolas',20),troughcolor = '#000000',
                           fg = '#FFFFFF', bg = '#096b1b',borderwidth=0,highlightthickness=0))
        self.inputs.append(Label(self.window,text=self.texts[self.language][0],font=('Arial',45),fg='#FFFFFF',bg='#096b1b',))
        self.inputs.append(Label(self.window,text=self.texts[self.language][1],font=('Arial',45),fg='#FFFFFF',bg='#096b1b',))
        coordinates = [[425,325],[350,225],[775,225],[810,400],[885,400],[810,325],[885,325]]
        for i in range(4): self.inputs.append( Radiobutton(self.window,variable=self.radio,value=i,image = self.images[i],
                        indicatoron=0,command=self.humanBid))
        if(isFirst == FALSE):
            self.inputs.append(Button(self.window,text="PASS",command=self.passTurn,font=("Comic Sans",30),fg="#FFFFFF",bg="black"))
            coordinates.append([575,325])
        for i in range(len(coordinates)) : self.inputs[i].place(x = coordinates[i][0],y=coordinates[i][1])
    
    def humanBid(self):
        types = ["spades","clubs","diamonds","hearts"]
        for i in range(4):
            if( self.radio.get() == i) : self.trump = types[i]
        self.bid = self.inputs[0].get()
        self.bidwinner = 0
        self.bidder = 3
        self.bidTurn = self.bidTurn +1
        for i in range(len(self.inputs)) : self.inputs[i].destroy()
        self.inputs.clear()
        self.biddingStage()

    def passTurn(self):
        self.bidTurn = self.bidTurn +1
        if(self.bidder == 0):
            self.bidder = 3
            for i in range(len(self.inputs)) : self.inputs[i].destroy()
            self.inputs.clear()
        else: 
            self.bidder = 2
            msg = ""
            if( self.language == 0) : msg = "Your mate has passed"
            else : msg = "Eşiniz pas geçti"
            messagebox.showinfo(title='Eşli Batak',message=msg)
        self.biddingStage()
        
    def cpuBid(self,cpu):
        if( cpu == 3) : self.bidder = 1
        elif (cpu == 1) : self.bidder = 2
        else : self.bidder = 0
        self.bidTurn = self.bidTurn +1
        suits = ["diamonds","spades","hearts","clubs"]
        amounts = [0,0,0,0]
        for i in range(4):
            for j in range(cpu*13,(cpu+1)*13):
                if( self.cards[j].type == suits[i]):
                     amounts[i] = amounts[i] +1
        takers = 0.0
        trumpIndex = amounts.index(max(amounts))
        for i in range(cpu*13,(cpu+1)*13):
                value = self.cards[i].value
                if(value == 14 or value == 13 or value == 12) : takers = takers + 1.0
        if((max(amounts)-4) > 0) : takers = takers + (max(amounts)-4)
        if( takers >= self.bid or self.bid == 6):
            self.bid = self.bid +1
            self.bidwinner = cpu
            msg = ""
            if( self.language == 0):
                if( cpu == 3) : msg += "The computer in right bidded\nNew bid is: "
                elif( cpu == 1) : msg += "Your mate bidded\nNew bid is: "
                elif( cpu == 2) : msg += "The computer in left bidded\nNew bid is: "
            else:
                if( cpu == 3) : msg += "Sağdaki bilgisayar ihaleye girdi\nYeni ihale: "
                elif( cpu == 1) : msg += "Eşiniz ihaleye girdi\nYeni ihale: "
                elif( cpu == 2) : msg += "Soldaki bilgisayar ihaleye girdi\nYeni ihale: "
            msg += str(self.bid)
            messagebox.showinfo(title='Eşli Batak',message=msg)
            self.cpuTrump =  suits[trumpIndex]
            self.biddingStage()
        else:
            msg = ""
            if( self.language == 0) : msg = "Computer has passed"
            else : msg = "Bilgisayar pas geçti"
            messagebox.showinfo(title='Eşli Batak',message=msg)
            self.biddingStage()
        
    def cardSelect(self,event): event.widget.place(x = event.widget.winfo_x(),y = event.widget.winfo_y() - 20)

    def cardDeselect(self,event):event.widget.place(x = event.widget.winfo_x(),y = event.widget.winfo_y() + 20)

    def humanPlay(self,event):
        label = event.widget
        index = self.labels.index(label)
        player = int(index/13)
        self.unbind(player)
        self.cardAnimation(label,index,player,TRUE)
        if( index < 13) : cpu = 4
        else : cpu = 3
        time.sleep(0.5)
        if( self.turn == 0):
            self.firstTurnInitialize(player)
            player = self.switchPlayers(player)
            self.turn = self.humanTurn(self.turn,player)
            self.cpuplay(cpu,player)
        elif( self.turn < 3):
            self.winnerCheck(player)
            player = self.switchPlayers(player)
            self.turn = self.humanTurn(self.turn,player)
            self.cpuplay(cpu,player)
        else: 
            self.winnerCheck(player)
            self.turn = 0
            self.turnEndAnimation()
            if( self.winner == 0 or self.winner == 1) : self.humanWin(self.winner)
            else:
                player = self.switchPlayers(player)
                self.cpuWin()
                
    def unbind(self,player):
        for i in range( player*13,(player+1)*13):
            if( self.labels[i] != None):
                self.labels[i].unbind("<Enter>")
                self.labels[i].unbind("<Leave>")
                self.labels[i].unbind("<Button-1>")

    def switchPlayers(self,player):
        if( player == 0) : return 1
        else : return 0

    def winnerCheck(self,player):
        if ( self.oldType == None and self.playedCards[self.turn].type == self.trump): 
            self.oldType = self.turnType
            self.turnType = str(self.trump)
        isGreatest = TRUE
        if( self.playedCards[self.turn].type != self.turnType) : isGreatest = FALSE
        else:
            for i in range(len(self.playedCards)):
                if(self.playedCards[i].type == self.turnType and 
                self.playedCards[i].value > self.playedCards[self.turn].value) : isGreatest = FALSE
        if ( isGreatest == TRUE): 
            self.greatest = self.playedCards[self.turn]
            self.winner = player

    def firstTurnInitialize(self,player):
        self.turnType = self.playedCards[0].type
        self.oldType = None
        self.winner = player
        self.greatest = self.playedCards[0]

    def turnEndAnimation(self): 
        for i in range(len(self.playedLabels)-1): self.playedLabels[i].destroy()
        end = self.playedLabels[len(self.playedLabels)-1]
        endx = end.winfo_x() ; endy = end.winfo_y()
        if( self.winner == 0):
            while( endy < 800): 
                endy += 2
                end.place( x = endx, y=endy)
                self.window.update()
        elif( self.winner == 1):
            while( endy > 0): 
                endy -= 2
                end.place( x = endx, y=endy)
                self.window.update()
        elif( self.winner == 2):
            while( endx > 0): 
                endx -= 2
                end.place( x = endx, y=endy)
                self.window.update()
        elif( self.winner == 3):
            while( endx < 1400): 
                endx += 2
                end.place( x = endx, y=endy)
                self.window.update()
        end.destroy()
        self.playedLabels.clear
        self.playedCards.clear()
        self.window.update()

    def scoreDisplay(self,isHuman,score):
        xpos = 0 ; ypos=0
        if( isHuman == TRUE) : xpos = 125 ; ypos=70
        else : xpos = 1245 ; ypos=70
        if ( score == 12) : score = 2
        if( score % 5 == 0) : ypos = ypos + (35 * int(score/5))
        elif (score %4 == 0): xpos = xpos - 70 ; ypos = ypos + (35 * int(score/5))
        elif (score %2 == 0) : xpos = xpos - 35 ; ypos = ypos + (35 * int(score/5))
        elif (score %3 == 0) : xpos = xpos + 70 ; ypos = ypos + (35 * int(score/5))
        else : xpos = xpos + 35 ; ypos = ypos + (35 * int(score/5))
        scoreLogo = Label(self.window,image=self.score,borderwidth=0,highlightthickness=0)
        scoreLogo.place( x = xpos , y = ypos)

    def cardAnimation(self,label,index,player,isHuman):
        animate = Label(self.window, image= self.cards[index].img,borderwidth=0,highlightthickness=0)
        if(isHuman == TRUE):
            for i in range(26):
                if( self.labels[i] != None):
                    self.labels[i].config(image=self.cards[i].img)
        xpos = label.winfo_x() ; ypos = label.winfo_y()
        xstep = (625 - label.winfo_x())/100 ; ystep = (270 - label.winfo_y())/100
        animate.place(x = xpos,y = ypos)
        label.destroy()
        self.labels[index] = None
        self.playedCards.append(self.cards[index])
        self.playedLabels.append(animate)
        for i in range(100):
            animate.place(x = xpos + xstep,y= ypos + ystep)
            xpos += xstep ; ypos +=ystep
            self.window.update()
        counter = 0
        if( isHuman == TRUE) : self.positions[2*player] = self.positions[2*player] + 30
        else : self.positions[2*player+1] = self.positions[2*player+1] + 20
        for i in range( player*13,(player+1)*13):
            if( self.labels[i] != None):
                if (isHuman == TRUE) : self.labels[i].place(x = self.positions[2*player] + 60*counter, y= self.positions[2*player+1])
                else : self.labels[i].place(x = self.positions[2*player], y= self.positions[2*player+1] + 40*counter)
                counter +=1
        self.window.update()

    def cpuplay(self,cpu,player):
        index = self.cpuTurn(cpu)
        label = self.labels[index]
        self.cardAnimation(label,index,cpu-1,FALSE)
        if( self.turn == 0):
            self.firstTurnInitialize(cpu-1)
            self.playableHumanCards(player)
            self.turn += 1
            
        elif( self.turn < 3):
            self.winnerCheck(cpu-1)
            self.playableHumanCards(player)
            self.turn += 1 
        else:
            self.winnerCheck(cpu-1)
            self.turn = 0
            self.turnEndAnimation()
            if( self.winner == 0 or self.winner == 1) : self.humanWin(self.winner)
            else: self.cpuWin()
            
    def cpuTurn(self,cpu):
        index = -1 ; value = 0
        if( self.oldType == None):
            for i in range((cpu-1)*13,cpu*13):
                if( self.labels[i] != None):
                    if (self.cards[i].type == self.turnType):
                        if(self.cards[i].value > value):
                            index = i
                            value = self.cards[i].value
            if( index == -1):
                for i in range((cpu-1)*13,cpu*13):
                    if( self.labels[i] != None):
                        if(self.cards[i].value > value):
                            index = i
                            value = self.cards[i].value
        else:
            for i in range((cpu-1)*13,cpu*13):
                if( self.labels[i] != None):
                    if (self.cards[i].type == self.oldType):
                        if(self.cards[i].value > value):
                            index = i
                            value = self.cards[i].value
            if( index == -1):
                for i in range((cpu-1)*13,cpu*13):
                    if( self.labels[i] != None):
                        if (self.cards[i].type == self.turnType):
                            if(self.cards[i].value > value):
                                index = i
                                value = self.cards[i].value
            if( index == -1):
                for i in range((cpu-1)*13,cpu*13):
                    if( self.labels[i] != None):
                        if(self.cards[i].value > value):
                            index = i
                            value = self.cards[i].value 
        return index

    def humanTurn(self,turn,player):
        for i in range( player*13,(player+1)*13) : self.activeCards[i] = FALSE
        return turn +1

    def humanWin(self,winner):
        player = winner
        self.humanScore +=1
        self.scoreDisplay(TRUE,self.humanScore-1)
        if( (self.humanScore + self.cpuScore) == 13) : self.gameOver()
        else: 
            for i in range( player*13,(player+1)*13):
                if( self.labels[i] != None):
                    self.labels[i].bind("<Enter>",self.cardSelect)
                    self.labels[i].bind("<Leave>",self.cardDeselect)
                    self.labels[i].bind("<Button-1>",self.humanPlay)
        
    def cpuWin(self):
        time.sleep(0.5)
        self.cpuScore += 1
        self.scoreDisplay(FALSE,self.cpuScore-1)
        if( (self.humanScore + self.cpuScore) == 13) : self.gameOver()
        if ( self.winner == 2) : 
            for i in range( (0)*13,(0+1)*13) : self.activeCards[i] = FALSE
            self.cpuplay(self.winner+1,0)
        else : 
            for i in range( (1)*13,(1+1)*13) : self.activeCards[i] = FALSE
            self.cpuplay(self.winner+1,1)

    def gameOver(self):
        self.window.destroy()
        
    def bind(self,label,i,marked):
        label.bind("<Enter>",self.cardSelect)
        label.bind("<Leave>",self.cardDeselect)
        label.bind("<Button-1>",self.humanPlay)
        self.activeCards[i] = TRUE
        return marked +1

    def playableHumanCards(self,player):
        marked = 0
        if( self.oldType == None):
            for i in range( player*13,(player+1)*13):
                if( self.labels[i] != None):
                        if(self.cards[i].type == self.turnType and 
                        self.cards[i].value > self.greatest.value): marked = self.bind(self.labels[i],i,marked)
            if( marked == 0):
                for i in range( player*13,(player+1)*13):
                    if( self.labels[i] != None):
                        if(self.cards[i].type == self.turnType): marked = self.bind(self.labels[i],i,marked)
        if( marked == 0):
            hastrump = FALSE
            for i in range( player*13,(player+1)*13):
                if( self.labels[i] != None):
                    if( self.cards[i].type == self.trump):
                        hastrump = TRUE
                        break
            hasOldType = FALSE
            if( self.oldType != None):
                for i in range( player*13,(player+1)*13):
                    if( self.labels[i] != None):
                        if( self.cards[i].type == self.oldType):
                            hasOldType = TRUE
                            break
            if ( self.oldType != None and hasOldType == TRUE):
                for i in range( player*13,(player+1)*13):
                    if( self.labels[i] != None and self.cards[i].type == self.oldType): self.bind(self.labels[i],i,marked)
            elif ( (self.oldType != None and hasOldType == FALSE) and hastrump == TRUE):
                for i in range( player*13,(player+1)*13):
                        if( (self.labels[i] != None and self.cards[i].type == self.trump) and
                             self.cards[i].value > self.greatest.value): self.bind(self.labels[i],i,marked)
                if( marked == 0):
                    for i in range( player*13,(player+1)*13):
                        if( self.labels[i] != None and self.cards[i].type == self.trump): self.bind(self.labels[i],i,marked)
            elif ( (self.oldType != None and hasOldType == FALSE) and hastrump == FALSE):
                for i in range( player*13,(player+1)*13):
                    if( self.labels[i] != None): self.bind(self.labels[i],i,marked)
            elif(self.oldType == None and hastrump == TRUE):
                for i in range( player*13,(player+1)*13):
                    if( self.labels[i] != None and self.cards[i].type == self.trump): self.bind(self.labels[i],i,marked)
            elif(self.oldType == None and hastrump == FALSE):
                for i in range( player*13,(player+1)*13):
                    if( self.labels[i] != None): self.bind(self.labels[i],i,marked)
        for i in range( player*13,(player+1)*13):
                if( self.labels[i] != None):
                    if( self.activeCards[i] == TRUE): self.labels[i].config(image=self.cards[i].img)
                    else : 
                        self.labels[i].config(image=self.cards[i].unplayable)

    def createLabels(self):
        coordinates = [275,598,275,20,40,89,1160,89]
        for i in range(len(coordinates)) : self.positions.append(coordinates[i])
        for i in range(4):
            if( i == 0 or i == 1):
                for j in range(13):
                    if(i==0): 
                        label = Label(self.window,image = self.cards[(13*i) + j].img,borderwidth=0, highlightthickness=0)
                        self.labels.append(label)
                        label.place(x = 275 + 60*j, y= 598)
                    else:  
                        label = Label(self.window,image = self.cardBackV,borderwidth=0, highlightthickness=0)
                        self.labels.append(label) 
                        label.place(x = 275 + 60*j, y= 20)
            elif( i == 2 or i == 3):
                for j in range(13):
                    label = Label(self.window,image = self.cardBackH,borderwidth=0, highlightthickness=0)
                    self.labels.append(label)
                    if( i == 2) : label.place(x = 40, y= 89 + 40*j)
                    else : label.place(x = 1160, y= 89 + 40*j)
    
    def getStarter(self):
        if( self.starter == 0) : return 3
        elif (self.starter == 3) : return 1
        elif (self.starter == 1) : return 2
        elif (self.starter == 2) : return 0
    
    def getScores(self):
        rtr = []
        if(self.bidwinner == 0 or self.bidwinner == 1):
            if(self.humanScore >= self.bid) : rtr.append(self.humanScore)
            else : rtr.append(-self.bid)
            if(self.cpuScore >= 2) : rtr.append(self.cpuScore)
            else : rtr.append(-self.bid)
        else:
            if(self.humanScore >= 2) : rtr.append(self.humanScore)
            else : rtr.append(-self.bid)
            if(self.cpuScore >= self.bid) : rtr.append(self.cpuScore)
            else : rtr.append(-self.bid)
        return rtr