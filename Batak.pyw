from tkinter import *
from tkinter import messagebox
from Card import *
import time
import random

window = Tk()
cards = []
labels = []
cardBackV = None
cardBackH = None
inputs = []
bid = None
trump = None
radio = IntVar()
images = []
positions = []
playedCards = []
greatest = None
playedLabels = []
turn = None
turnType = None
winner = None
humanScore = None
cpuScore = None
scoreBoard = None
activeCards = []

def main():
    loadImages()
    createWindow()
    createCards()
    sortCards()
    createLabels()
    Settings()
    window.mainloop()

def loadImages():
    global cardBackV
    global cardBackH
    global activeCards
    for i in range(52) : activeCards.append(FALSE)
    cardBackV =PhotoImage(file = "img/back_v.png") ; cardBackH =PhotoImage(file = "img/back.png")
    Suits = [PhotoImage(file = "img/Logo.png"),PhotoImage(file = "img/Club.png"),PhotoImage(file = "img/Diamond.png"),
             PhotoImage(file = "img/Heart.png")]
    for i in range(4) : images.append(Suits[i])

def createWindow():
    window.geometry("1400x800")
    window.title("Batak")
    window.iconphoto(True,PhotoImage(file="img/Logo.png"))
    window.config(background="#096b1b")
    window.resizable(height=False,width=False)

def createCards():
    types = ["clubs","diamonds","spades","hearts"]
    Values = ["jack","queen","king","ace"]
    for i in range(4):
        for j in range(2,15):
            path  = "img/"
            if(j<11): path += str(j)
            else : path += Values[j-11]
            path += "_of_" + types[i] + ".png"
            cards.append(Card(j,types[i],path))
    random.shuffle(cards)
    
def sortCards():
    global cards
    newCards = []
    types = ["spades","hearts","diamonds","clubs"]
    spades = [] ; hearts = [] ; diamonds = [] ; clubs = []    
    suits = [spades,hearts,diamonds,clubs]
    for i in range(4):
        for j in range(13):
            card = cards[ (13*i) + j ]
            for k in range(4) : 
                if(card.type == types[k]) :suits[k].append(card)
        for j in range (4) : suits[j].sort(key= lambda item : item.value)
        for j in range(4):
            for k in range(len(suits[j])):
                newCards.append(suits[j][k])
        for j in range(4) : suits[j].clear()
    cards = newCards
                
def Settings():
    global inputs
    inputs.append(Scale(window,from_=7,to=13,length=220,font = ('Consolas',20),troughcolor = '#000000',fg = '#FFFFFF',bg = '#096b1b',
                  borderwidth=0,highlightthickness=0))
    inputs.append(Label(window,text="Your bid ?",font=('Arial',45),fg='#FFFFFF',bg='#096b1b',))
    inputs.append(Label(window,text="Trump ?",font=('Arial',45),fg='#FFFFFF',bg='#096b1b',))
    coordinates = [[425,325],[350,225],[775,225],[810,400],[885,400],[810,325],[885,325]]
    for i in range(4): inputs.append( Radiobutton(window,variable=radio,value=i,image = images[i],indicatoron=0,command=begin)) 
    for i in range(len(coordinates)) : inputs[i].place(x = coordinates[i][0],y=coordinates[i][1])
    
def begin():
    global bid
    global inputs
    global trump
    global turn
    global humanScore
    global cpuScore
    global scoreBoard
    bid = inputs[0].get()
    types = ["spades","clubs","diamonds","hearts"]
    for i in range(4):
        if( radio.get() == i) : trump = types[i]
    for i in range(len(inputs)) : inputs[i].destroy()
    for i in range(13,26) : labels[i].config(image=cards[i].img)
    inputs.clear()
    turnType = "Beginning"
    turn = 0 ; humanScore = 0 ; cpuScore = 0
    scoreBoard = Label(window,text= "Tricks: " + str(humanScore),font=('Arial',30),fg='#FFFFFF',bg='#096b1b')
    scoreBoard.place(x = 1150 , y = 20)
    for i in range(13):
        labels[i].bind("<Enter>",cardSelect)
        labels[i].bind("<Leave>",cardDeselect)
        labels[i].bind("<Button-1>",cardPlay)
    
def cardSelect(event): event.widget.place(x = event.widget.winfo_x(),y = event.widget.winfo_y() - 20)

def cardDeselect(event):event.widget.place(x = event.widget.winfo_x(),y = event.widget.winfo_y() + 20)

def cardPlay(event):
    global labels
    global turnType
    global turn
    global winner
    global humanScore
    global cpuScore
    global greatest
    global activeCards
    label = event.widget
    index = labels.index(label)
    player = int(index/13)
    unbind(player)
    cardAnimation(label,index,player,TRUE)
    if( index < 13) : cpu = 4
    else : cpu = 3
    time.sleep(0.5)
    if( turn == 0):
        firstTurnInitialize(player)
        player = switchPlayers(player)
        turn = humanTurn(turn,player)
        cpuplay(cpu,player)
    elif( turn < 3):
        winnerCheck(player)
        player = switchPlayers(player)
        turn = humanTurn(turn,player)
        cpuplay(cpu,player)
    else: 
        winnerCheck(player)
        turn = 0
        turnEndAnimation()
        if( winner == 0 or winner == 1) : humanWin(winner)
        else:
            player = switchPlayers(player)
            cpuWin()
            
def unbind(player):
    global labels
    for i in range( player*13,(player+1)*13):
         if( labels[i] != None):
             labels[i].unbind("<Enter>")
             labels[i].unbind("<Leave>")
             labels[i].unbind("<Button-1>")

def switchPlayers(player):
    if( player == 0) : return 1
    else : return 0

def winnerCheck(player):
    global greatest
    global winner
    if ( playedCards[turn].type == trump): 
        turnType = str(trump)
        isGreatest = TRUE
        if( playedCards[turn].type != turnType) : isGreatest = FALSE
        else:
            for i in range(len(playedCards)):
                if(playedCards[i].type == turnType and playedCards[i].value > playedCards[turn].value) : isGreatest = FALSE
        if ( isGreatest == TRUE): 
            greatest = playedCards[turn]
            winner = player

def firstTurnInitialize(player):
    global turnType
    global winner
    global greatest
    turnType = playedCards[0].type
    winner = player
    greatest = playedCards[0]

def turnEndAnimation(): 
    global playedLabels
    global winner
    for i in range(len(playedLabels)-1): playedLabels[i].destroy()
    end = playedLabels[len(playedLabels)-1]
    endx = end.winfo_x() ; endy = end.winfo_y()
    if( winner == 0):
        while( endy < 800): 
            endy += 2
            end.place( x = endx, y=endy)
            window.update()
    elif( winner == 1):
        while( endy > 0): 
            endy -= 2
            end.place( x = endx, y=endy)
            window.update()
    elif( winner == 2):
        while( endx > 0): 
            endx -= 2
            end.place( x = endx, y=endy)
            window.update()
    elif( winner == 3):
        while( endx < 1400): 
            endx += 2
            end.place( x = endx, y=endy)
            window.update()
    end.destroy()
    playedLabels.clear
    playedCards.clear()
    window.update()

def cardAnimation(label,index,player,isHuman):
    animate = Label(window, image= cards[index].img)
    if(isHuman == TRUE):
        for i in range(26):
            if( labels[i] != None):
                labels[i].config(image=cards[i].img)
    xpos = label.winfo_x() ; ypos = label.winfo_y()
    xstep = (625 - label.winfo_x())/100 ; ystep = (270 - label.winfo_y())/100
    animate.place(x = xpos,y = ypos)
    label.destroy()
    labels[index] = None
    playedCards.append(cards[index])
    playedLabels.append(animate)
    for i in range(100):
        animate.place(x = xpos + xstep,y= ypos + ystep)
        xpos += xstep ; ypos +=ystep
        window.update()
    counter = 0
    if( isHuman == TRUE) : positions[2*player] = positions[2*player] + 30
    else : positions[2*player+1] = positions[2*player+1] + 20
    for i in range( player*13,(player+1)*13):
        if( labels[i] != None):
            if (isHuman == TRUE) : labels[i].place(x = positions[2*player] + 60*counter, y= positions[2*player+1])
            else : labels[i].place(x = positions[2*player], y= positions[2*player+1] + 40*counter)
            counter +=1
    window.update()

def cpuplay(cpu,player):
    global turnType
    global activeCards
    global labels
    global turn
    global winner
    global humanScore
    global cpuScore
    global greatest
    index = cpuTurn(cpu)
    label = labels[index]
    cardAnimation(label,index,cpu-1,FALSE)
    if( turn == 0):
        firstTurnInitialize(cpu-1)
        playableHumanCards(player)
        turn += 1
        
    elif( turn < 3):
        winnerCheck(cpu-1)
        playableHumanCards(player)
        turn += 1 
    else:
        winnerCheck(cpu-1)
        turn = 0
        turnEndAnimation()
        if( winner == 0 or winner == 1) : humanWin(winner)
        else: cpuWin()
        
def cpuTurn(cpu):
    index = -1 ; value = 0
    for i in range((cpu-1)*13,cpu*13):
        if( labels[i] != None):
            if (cards[i].type == turnType):
                if(cards[i].value > value):
                    index = i
                    value = cards[i].value
    if( index == -1):
        for i in range((cpu-1)*13,cpu*13):
            if( labels[i] != None):
                if(cards[i].value > value):
                    index = i
                    value = cards[i].value
    return index

def humanTurn(turn,player):
    for i in range( player*13,(player+1)*13) : activeCards[i] = FALSE
    return turn +1

def humanWin(winner):
    global humanScore
    player = winner
    humanScore +=1
    if( (humanScore + cpuScore) == 13) : gameOver()
    scoreBoard.config(text = "Tricks: " + str(humanScore))
    for i in range( player*13,(player+1)*13):
        if( labels[i] != None):
            labels[i].bind("<Enter>",cardSelect)
            labels[i].bind("<Leave>",cardDeselect)
            labels[i].bind("<Button-1>",cardPlay)
    
def cpuWin():
    global cpuScore
    time.sleep(0.5)
    cpuScore += 1
    if( (humanScore + cpuScore) == 13) : gameOver()
    scoreBoard.config(text = "Tricks: " + str(humanScore))
    if ( winner == 2) : 
        for i in range( (0)*13,(0+1)*13) : activeCards[i] = FALSE
        cpuplay(winner+1,0)
    else : 
        for i in range( (1)*13,(1+1)*13) : activeCards[i] = FALSE
        cpuplay(winner+1,1)

def gameOver():
    global humanScore
    global bid
    if(humanScore >= bid) : messagebox.showinfo(title="Game over",message="You have WON !")
    else: messagebox.showerror(title="Game over",message="You have LOST !")
    window.destroy()
    
def bind(label,i,marked):
    global activeCards
    label.bind("<Enter>",cardSelect)
    label.bind("<Leave>",cardDeselect)
    label.bind("<Button-1>",cardPlay)
    activeCards[i] = TRUE
    return marked +1

def playableHumanCards(player):
    global turnType
    global greatest
    global activeCards
    global labels
    global cards
    marked = 0
    for i in range( player*13,(player+1)*13):
        if( labels[i] != None):
                if(cards[i].type == turnType and cards[i].value > greatest.value): marked = bind(labels[i],i,marked)
        if( marked == 0):
            for i in range( player*13,(player+1)*13):
                if( labels[i] != None):
                        if(cards[i].type == turnType): marked = bind(labels[i],i,marked)
        if( marked == 0):
            hastrump = FALSE
            for i in range( player*13,(player+1)*13):
                if( labels[i] != None):
                    if( cards[i].type == trump):
                        hastrump = TRUE
                        break
            if( turnType == trump and hastrump == TRUE):
                 for i in range( player*13,(player+1)*13):
                    if( labels[i] != None and cards[i].type == trump): bind(labels[i],i,marked)
            elif(turnType == trump and hastrump == FALSE):
                for i in range( player*13,(player+1)*13):
                    if( labels[i] != None): bind(labels[i],i,marked)
            elif(turnType != trump and hastrump == TRUE):
                for i in range( player*13,(player+1)*13):
                    if( labels[i] != None and cards[i].type == trump): bind(labels[i],i,marked)
            elif(turnType != trump and hastrump == FALSE):
                for i in range( player*13,(player+1)*13):
                    if( labels[i] != None): bind(labels[i],i,marked)
    for i in range( player*13,(player+1)*13):
            if( labels[i] != None):
                if( activeCards[i] == TRUE): labels[i].config(image=cards[i].img)
                else : 
                    labels[i].config(image=cards[i].unplayable)

def createLabels():
    global cardBackV
    global cardBackH
    coordinates = [275,598,275,20,40,89,1160,89]
    for i in range(len(coordinates)) : positions.append(coordinates[i])
    for i in range(4):
        if( i == 0 or i == 1):
            for j in range(13):
                if(i==0): 
                    label = Label(window,image =cards[(13*i) + j].img,borderwidth=0, highlightthickness=0)
                    labels.append(label)
                    label.place(x = 275 + 60*j, y= 598)
                else:  
                    label = Label(window,image = cardBackV,borderwidth=0, highlightthickness=0)
                    labels.append(label) 
                    label.place(x = 275 + 60*j, y= 20)
        elif( i == 2 or i == 3):
            for j in range(13):
                label = Label(window,image = cardBackH,borderwidth=0, highlightthickness=0)
                labels.append(label)
                if( i == 2) : label.place(x = 40, y= 89 + 40*j)
                else : label.place(x = 1160, y= 89 + 40*j)
                
if __name__ == "__main__":
    main()