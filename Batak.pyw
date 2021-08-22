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
    createWindow()
    createCards()
    sortCards()
    createLabels()
    Settings()
    
    window.mainloop()

def createWindow():
    global cardBackV
    global cardBackH
    global activeCards
    for i in range(52) : activeCards.append(FALSE)
    Spade = PhotoImage(file = "img/Logo.png")
    Club = PhotoImage(file = "img/Club.png")
    Diamond = PhotoImage(file = "img/Diamond.png")
    Heart = PhotoImage(file = "img/Heart.png")
    cardBackV =PhotoImage(file = "img/back_v.png")
    cardBackH =PhotoImage(file = "img/back.png")
    images.append(Spade)
    images.append(Club)
    images.append(Diamond)
    images.append(Heart)
    window.geometry("1400x800")
    window.title("Batak")
    icon = PhotoImage(file="img/Logo.png")
    window.iconphoto(True,icon)
    window.config(background="#096b1b")
    window.resizable(height=False,width=False)


def createCards():
    path = ""
    type = ""
    for i in range(4):
        if(i == 0): type = "clubs"
        elif(i==1): type = "diamonds"
        elif(i==2): type = "spades"
        elif(i==3): type = "hearts"
        for j in range(2,15):
            path +="img/"
            if(j<11): path += str(j)
            elif(j == 11): path += str("jack")
            elif(j == 12): path += str("queen")
            elif(j == 13): path += str("king")
            elif(j == 14): path += str("ace")
            path += "_of_"
            path += type
            path += ".png"
            card = Card(j,type,path)
            cards.append(card)
            path = ""
            
    random.shuffle(cards)
    
def sortCards():
    newCards = []
    global cards
    for i in range(4):
        spades = []
        hearts = []
        diamonds = []
        clubs = []
        for j in range(13):
            card = cards[ (13*i) + j]
            if( card.type == "spades"): spades.append(card)
            elif( card.type == "hearts"): hearts.append(card)
            elif( card.type == "diamonds"): diamonds.append(card)
            elif( card.type == "clubs"):  clubs.append(card)
        for j in range(len(spades)-1):
            for k in range(len(spades)-1):
                if( spades[k].value > spades[k+1].value) :
                    temp = spades[k+1]
                    spades[k+1] = spades[k]
                    spades[k] = temp
        for j in range(len(hearts)-1):
            for k in range(len(hearts)-1):
                if( hearts[k].value > hearts[k+1].value) :
                    temp = hearts[k+1]
                    hearts[k+1] = hearts[k]
                    hearts[k] = temp
        for j in range(len(diamonds)-1):
            for k in range(len(diamonds)-1):
                if( diamonds[k].value > diamonds[k+1].value) :
                    temp = diamonds[k+1]
                    diamonds[k+1] = diamonds[k]
                    diamonds[k] = temp
        for j in range(len(clubs)-1):
            for k in range(len(clubs)-1):
                if( clubs[k].value > clubs[k+1].value) :
                    temp = clubs[k+1]
                    clubs[k+1] = clubs[k]
                    clubs[k] = temp
        for j in range( len(spades)) : newCards.append(spades[j])
        for j in range( len(diamonds)) : newCards.append(diamonds[j])
        for j in range( len(clubs)) : newCards.append(clubs[j])
        for j in range( len(hearts)) : newCards.append(hearts[j])
        
    cards = newCards
                
def Settings():
    scale = Scale(window,from_=7,to=13,length=220,
              font = ('Consolas',20),
              troughcolor = '#000000',
              relief= None,
              highlightbackground='#096b1b',
              fg = '#FFFFFF',
              bg = '#096b1b'
              )
    inputs.append(scale)
    scale.place(x = 425, y = 325)
    label1 = Label(window,
              text="Your bid ?",
              font=('Arial',45),
              fg='#FFFFFF',
              bg='#096b1b',)
    inputs.append(label1)
    label1.place(x = 350, y = 225)
    label2 = Label(window,
              text="Trump ?",
              font=('Arial',45),
              fg='#FFFFFF',
              bg='#096b1b',)
    inputs.append(label2)
    label2.place(x = 775, y = 225)
    
    for i in range(4):
        radiobutton = Radiobutton(window,variable=radio,value=i,image = images[i],indicatoron=0,command=begin)
        inputs.append(radiobutton)
    inputs[3].place( x = 810, y = 400 )
    inputs[4].place( x = 885, y = 400 )
    inputs[5].place( x = 810, y = 325 )
    inputs[6].place( x = 885, y = 325 )



def begin():
    global bid
    bid = inputs[0].get()
    global trump
    if( radio.get() == 0) : trump = "spades"
    elif( radio.get() == 1) : trump = "clubs"
    elif( radio.get() == 2) : trump = "diamonds"
    elif( radio.get() == 3) : trump = "hearts"
    for i in range(len(inputs)) : inputs[i].destroy()
    for i in range(13,26) : labels[i].config(image=cards[i].img)
    window.update()
    turnType = "Beginning"
    global turn
    global humanScore
    global cpuScore
    turn = 0
    humanScore = 0
    cpuScore = 0
    global scoreBoard
    scoreBoard = Label(window,
              text= "Tricks: " + str(humanScore),
              font=('Arial',30),
              fg='#FFFFFF',
              bg='#096b1b',)
    scoreBoard.place(x = 1150 , y = 20)
    for i in range(13):
        label = labels[i]
        label.bind("<Enter>",cardSelect)
        label.bind("<Leave>",cardDeselect)
        label.bind("<Button-1>",cardPlay)
    

def cardSelect(event):
    label = event.widget
    label.place(x = label.winfo_x(),y = label.winfo_y() - 20)

def cardDeselect(event):
    label = event.widget
    label.place(x = label.winfo_x(),y = label.winfo_y() + 20)

def cardPlay(event):
    global labels
    label = event.widget
    index = labels.index(label)
    player = int(index/13)
    for i in range( player*13,(player+1)*13):
         if( labels[i] != None):
             labels[i].unbind("<Enter>")
             labels[i].unbind("<Leave>")
             labels[i].unbind("<Button-1>")
    animate = Label(window, image= cards[index].img)
    for i in range(26):
        if( labels[i] != None):
            labels[i].config(image=cards[i].img)
    if( index < 13) : cpu = 4
    else : cpu = 3
    xpos = label.winfo_x()
    ypos = label.winfo_y()
    xstep = (625 - label.winfo_x())/100
    ystep = (270 - label.winfo_y())/100
    animate.place(x = xpos,y = ypos)
    label.destroy()
    labels[index] = None
    playedCards.append(cards[index])
    playedLabels.append(animate)
    for i in range(100):
        animate.place(x = xpos + xstep,y= ypos + ystep)
        xpos += xstep
        ypos +=ystep
        window.update()
    counter = 0
    positions[2*player] = positions[2*player] + 30
    for i in range( player*13,(player+1)*13):
        if( labels[i] != None):
            labels[i].place(x = positions[2*player] + 60*counter, y= positions[2*player+1])
            counter +=1
    time.sleep(0.5)
    global turnType
    global turn
    global winner
    global humanScore
    global cpuScore
    global greatest
    global activeCards
    if( turn == 0):
        turnType = playedCards[0].type
        winner = player
        turn += 1
        if( player == 0) : player = 1
        else : player = 0
        greatest = playedCards[0]
        for i in range( player*13,(player+1)*13) : activeCards[i] = FALSE
        cpuplay(cpu,player)
    elif( turn < 3):
        if ( playedCards[turn].type == trump): 
            turnType = str(trump)
        isGreatest = TRUE
        if( playedCards[turn].type != turnType) : isGreatest = FALSE
        else:
            for i in range(len(playedCards)):
                if(playedCards[i].type == turnType and playedCards[i].value > playedCards[turn].value) : isGreatest = FALSE
        if( isGreatest == TRUE): 
            greatest = playedCards[turn]
            winner = player
        turn += 1
        if( player == 0) : player = 1
        else : player = 0
        for i in range( player*13,(player+1)*13) : activeCards[i] = FALSE
        cpuplay(cpu,player)
    else: 
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
        turn = 0
        for i in range(len(playedLabels)-1): playedLabels[i].destroy()
        end = playedLabels[len(playedLabels)-1]
        endx = end.winfo_x()
        endy = end.winfo_y()
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
            while( endx < 800): 
                endx += 2
                end.place( x = endx, y=endy)
                window.update()
        end.destroy()
        playedLabels.clear
        playedCards.clear()
        window.update()
        if( winner == 0 or winner == 1) : 
            player = winner
            humanScore +=1
            if( (humanScore + cpuScore) == 13) : gameOver()
            message = "Tricks: " + str(humanScore)
            scoreBoard.config(text = str(message))
            for i in range( player*13,(player+1)*13):
                if( labels[i] != None):
                    labels[i].bind("<Enter>",cardSelect)
                    labels[i].bind("<Leave>",cardDeselect)
                    labels[i].bind("<Button-1>",cardPlay)
        else:
            time.sleep(0.5)
            cpuScore += 1
            if( (humanScore + cpuScore) == 13) : gameOver()
            if( player == 0) : player = 1
            else : player = 0
            message = "Tricks: " + str(humanScore)
            scoreBoard.config(text = str(message))
            if ( winner == 2) : 
                for i in range( (0)*13,(0+1)*13) : activeCards[i] = FALSE
                cpuplay(winner+1,0)
            else : 
                for i in range( (1)*13,(1+1)*13) : activeCards[i] = FALSE
                cpuplay(winner+1,1)
            
    

def cpuplay(cpu,player):
    index = -1
    value = 0
    global turnType
    global activeCards
    global labels
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
    label = labels[index]
    animate = Label(window, image= cards[index].img)
    xpos = label.winfo_x()
    ypos = label.winfo_y()
    xstep = (625 - label.winfo_x())/100
    ystep = (270 - label.winfo_y())/100
    animate.place(x = xpos,y = ypos)
    label.destroy()
    labels[index] = None
    playedCards.append(cards[index])
    playedLabels.append(animate)
    for i in range(100):
        animate.place(x = xpos + xstep,y= ypos + ystep)
        xpos += xstep
        ypos +=ystep
        window.update()
    counter = 0
    positions[2*(cpu-1)+1] = positions[2*(cpu-1)+1] + 20
    for i in range( (cpu-1)*13,((cpu-1)+1)*13):
        if( labels[i] != None):
            labels[i].place(x = positions[2*(cpu-1)], y= positions[2*(cpu-1)+1] + 40*counter)
            counter +=1
    window.update()
    global turn
    global winner
    global humanScore
    global cpuScore
    global greatest
    if( turn == 0):
        turnType = playedCards[0].type
        winner = cpu-1
        marked = 0
        greatest = playedCards[0]
        for i in range( player*13,(player+1)*13):
            if( labels[i] != None):
                    if(cards[i].type == turnType and cards[i].value > greatest.value):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
                        marked +=1
        if( marked == 0):
            for i in range( player*13,(player+1)*13):
                if( labels[i] != None):
                        if(cards[i].type == turnType):
                            labels[i].bind("<Enter>",cardSelect)
                            labels[i].bind("<Leave>",cardDeselect)
                            labels[i].bind("<Button-1>",cardPlay)
                            activeCards[i] = TRUE
                            marked +=1
        if( marked == 0):
            hastrump = FALSE
            for i in range( player*13,(player+1)*13):
                if( labels[i] != None):
                    if( cards[i].type == trump):
                        hastrump = TRUE
                        break
            if( turnType == trump and hastrump == TRUE):
                 for i in range( player*13,(player+1)*13):
                    if( labels[i] != None and cards[i].type == trump):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
            elif(turnType == trump and hastrump == FALSE):
                for i in range( player*13,(player+1)*13):
                    if( labels[i] != None):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
            elif(turnType != trump and hastrump == TRUE):
                for i in range( player*13,(player+1)*13):
                    if( labels[i] != None and cards[i].type == trump):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
            elif(turnType != trump and hastrump == FALSE):
                for i in range( player*13,(player+1)*13):
                    if( labels[i] != None):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
        turn += 1
        for i in range( player*13,(player+1)*13):
            if( labels[i] != None):
                if( activeCards[i] == TRUE): labels[i].config(image=cards[i].img)
                else : 
                    print("burdayim")
                    labels[i].config(image=cards[i].unplayable)
        window.update()
    elif( turn < 3):
        if ( playedCards[turn].type == trump): 
            turnType = str(trump)
        isGreatest = TRUE
        if( playedCards[turn].type != turnType) : isGreatest = FALSE
        else:
            for i in range(len(playedCards)):
                if(playedCards[i].type == turnType and playedCards[i].value > playedCards[turn].value) : isGreatest = FALSE
        if( isGreatest == TRUE): 
            greatest = playedCards[turn]
            winner = cpu-1
        marked = 0
        for i in range( player*13,(player+1)*13):
            if( labels[i] != None):
                    if(cards[i].type == turnType and cards[i].value > greatest.value):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
                        marked +=1
        if( marked == 0):
            for i in range( player*13,(player+1)*13):
                if( labels[i] != None):
                        if(cards[i].type == turnType):
                            labels[i].bind("<Enter>",cardSelect)
                            labels[i].bind("<Leave>",cardDeselect)
                            labels[i].bind("<Button-1>",cardPlay)
                            activeCards[i] = TRUE
                            marked +=1
        if( marked == 0):
            hastrump = FALSE
            for i in range( player*13,(player+1)*13):
                if( labels[i] != None):
                    if( cards[i].type == trump):
                        hastrump = TRUE
                        break
            if( turnType == trump and hastrump == TRUE):
                 for i in range( player*13,(player+1)*13):
                    if( labels[i] != None and cards[i].type == trump):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
            elif(turnType == trump and hastrump == FALSE):
                for i in range( player*13,(player+1)*13):
                    if( labels[i] != None):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
            elif(turnType != trump and hastrump == TRUE):
                for i in range( player*13,(player+1)*13):
                    if( labels[i] != None and cards[i].type == trump):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
            elif(turnType != trump and hastrump == FALSE):
                for i in range( player*13,(player+1)*13):
                    if( labels[i] != None):
                        labels[i].bind("<Enter>",cardSelect)
                        labels[i].bind("<Leave>",cardDeselect)
                        labels[i].bind("<Button-1>",cardPlay)
                        activeCards[i] = TRUE
        turn += 1
        for i in range( player*13,(player+1)*13):
            if( labels[i] != None):
                if( activeCards[i] == TRUE): labels[i].config(image=cards[i].img)
                else : 
                    print("burdayim")
                    labels[i].config(image=cards[i].unplayable)       
        window.update()
    else:
        if ( playedCards[turn].type == trump): 
            turnType = str(trump)
        isGreatest = TRUE
        if( playedCards[turn].type != turnType) : isGreatest = FALSE
        else:
            for i in range(len(playedCards)):
                if(playedCards[i].type == turnType and playedCards[i].value > playedCards[turn].value) : isGreatest = FALSE
        if ( isGreatest == TRUE): 
            greatest = playedCards[turn]
            winner = cpu-1
        turn = 0
        for i in range(len(playedLabels)-1): playedLabels[i].destroy()
        end = playedLabels[len(playedLabels)-1]
        endx = end.winfo_x()
        endy = end.winfo_y()
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
            while( endx < 800): 
                endx += 2
                end.place( x = endx, y=endy)
                window.update()
        end.destroy()
        playedLabels.clear
        playedCards.clear()
        window.update()
        if( winner == 0 or winner == 1) : 
            player = winner
            humanScore +=1
            if( (humanScore + cpuScore) == 13) : gameOver()
            message = "Tricks: " + str(humanScore)
            scoreBoard.config(text = str(message))
            for i in range( player*13,(player+1)*13):
                if( labels[i] != None):
                    labels[i].bind("<Enter>",cardSelect)
                    labels[i].bind("<Leave>",cardDeselect)
                    labels[i].bind("<Button-1>",cardPlay)
        else:
            time.sleep(0.5)
            cpuScore +=1
            if( (humanScore + cpuScore) == 13) : gameOver()
            message = "Tricks: " + str(humanScore)
            scoreBoard.config(text = str(message))
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
    

def createLabels():
    global cardBackV
    global cardBackH
    positions.append(275)
    positions.append(598)
    positions.append(275)
    positions.append(20)
    positions.append(40)
    positions.append(89)
    positions.append(1160)
    positions.append(89)
    for i in range(4):
        if( i == 0 or i == 1):
            for j in range(13):
                if(i==0) : label = Label(window,image =cards[(13*i) + j].img,borderwidth=0, highlightthickness=0)
                else : label = Label(window,image = cardBackV,borderwidth=0, highlightthickness=0)
                labels.append(label)
                if( i == 0) : label.place(x = 275 + 60*j, y= 598)
                else : label.place(x = 275 + 60*j, y= 20)
                
        elif( i == 2 or i == 3):
            for j in range(13):
                label = Label(window,image = cardBackH,borderwidth=0, highlightthickness=0)
                labels.append(label)
                if( i == 2) : label.place(x = 40, y= 89 + 40*j)
                else : label.place(x = 1160, y= 89 + 40*j)
                



    

if __name__ == "__main__":
    main()