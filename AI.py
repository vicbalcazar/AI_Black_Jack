import deck
import Player
#import pygame, os, time

def drawCard(hand, gDeck):
    hand.addCard(gDeck.draw())

#FUNCTIONS THAT CHECK THE STATE OF THE GAME(TECHNICALLY)===============================
"""Checks if either or both players got BlackJack"""
def checkBlackJack(pHandValue, bHandValue):
    if pHandValue == 21 and bHandValue == 21:
        return "tie blackjack", 3
    elif pHandValue == 21 and bHandValue != 21:
        return "player win blackjack", 0
    elif pHandValue != 21 and bHandValue == 21:
        return "dealer win blackjack", 1
    return "no", 2
"""Checks if either player goes over 21 and loses"""
def checkIfBust(pHandValue, bHandValue):
    if pHandValue > 21 and bHandValue < 21:
        return "player1 bust", 1
    elif bHandValue > 21 and pHandValue < 21:
        return "player2 bust", 0
    else:
        return "no", 2
"""Checks who got the most hand value at the end of the round"""
def checkWhoWon (pHandValue, bHandValue):
    if pHandValue == bHandValue and pHandValue <= 21:
        return "tie", 3
    elif pHandValue > bHandValue and pHandValue <= 21:
        return "player1 win", 0
    else:
        return "player2 win", 1

"""Enemy AI,Agressive"""
def dealerAIAgressive(dealer):
    """Enemy AI,Agressive
        Grab Card if value less than 18"""
    if dealer.value <= 17:
        playerDraw(dealer, deck1)
def dealerAIPassive(dealer):
    if dealer.value <= 14:
        playerDraw(dealer, deck1)

def declare_victory(Player):
    print (Player.name, "won the round!\n\n")
    Player.wins += 1

def playerDraw(player, myDeck):
    player.addCard(myDeck.draw())

def checkHandState(handState, p1, p2):
    if (handState == 0):
        p1.wins += 1
        return True
    elif (handState == 1):
        p2.wins += 1
        return True
    elif (handState == 3):
        return True
    else:
        return False


#AI SECTION, ARTIFICIAL NEURON
def continue_choice(Player):
    score = Player.value
    aces = Player.aces
    return (score - 2*aces) < Player.threshold

def overdraft_correction(Player):
    print (Player.name, "has made an overdraft")
    Player.threshold -= 1
    print(Player.name, "has had the threshold corrected to : ", Player.threshold)

def underdraft_correction(Player):
    print (Player.name, "has made an underdraft")
    Player.threshold +=1
    print(Player.name, "has had the threshold corrected to : ", Player.threshold)

class BlackJack:
    

    def __init__(self):
        self.myDeck = deck.Deck()
        #Artificial Neuron AI
        self.p1 = Player.Player("Player1", 15)
        self.p2 = Player.Player("Player2", 5)
        p1Continue = False
        p2Continue = False

    def initialDraw(self):
        for x in xrange(0,2):
            playerDraw(self.p1, self.myDeck)
            playerDraw(self.p2, self.myDeck)
        print self.p1
        print self.p2
        #print self.myDeck.size()

    def singleHand(self):
        handEnd = False
        state = 0
        msg = ""
        while(handEnd == False):
            self.p1Continue = continue_choice(self.p1)
            if (self.p1Continue):
                playerDraw(self.p1, self.myDeck)
                print self.p1
                msg, state = checkIfBust(self.p1.value, self.p2.value)
                #if (self.p1.value > 21):
                #    overdraft_correction(self.p1)
                handEnd = checkHandState(state, self.p1, self.p2)
            if (handEnd):
                continue
                
            #P1 decides whether to continue or not
            self.p2Continue = continue_choice(self.p2)

            if (self.p2Continue):
                playerDraw(self.p1, self.myDeck)
                print self.p2
                msg, state = checkIfBust(self.p1.value, self.p2.value)
                #if (self.p2.value > 21):
                #    overdraft_correction(self.p2)
                handEnd = checkHandState(state, self.p1, self.p2)
            if (handEnd):
                continue

            if (self.p1Continue == False and self.p1Continue == False):
                msg, state = checkWhoWon(self.p1.value, self.p2.value)
                handEnd = checkHandState(state, self.p1, self.p2)
        #if(self.p1.value > self.p2.value):
        #    underdraft_correction(self.p2)
        #else:
        #    underdraft_correction(self.p1)
        print msg

    def singleHandBlackJack(self):
        if (self.myDeck.size()) < 13:
            self.myDeck.renew()
        self.initialDraw()
        self.singleHand()

        for card in self.p1.hand:
            self.myDeck.discard.append(card)
        self.p1.clear()
        #deck1.discard.append(me.hand)
        for card in self.p2.hand:
            self.myDeck.discard.append(card)
        self.p2.clear()

    def blackJack(self):
        """Plays a full game of BlackJack, with proper rules"""
        self.myDeck.renew()
        trainingWinsP1 = self.p1.wins
        trainingWinsP2 = self.p2.wins

        while (self.myDeck.size() > 13):
            self.singleHandBlackJack()
        if ((self.p1.wins - trainingWinsP1) > (self.p2.wins - trainingWinsP2)):
            print "Player1 won"
        else:
            print "player2 Won"

    def singleHandTraining(self):
        """Trains AI for one round"""
        if (self.myDeck.size()) < 13:
            self.myDeck.renew()
        self.initialDraw()
        self.trainAI()

        for card in self.p1.hand:
            self.myDeck.discard.append(card)
        self.p1.clear()
        #deck1.discard.append(me.hand)
        for card in self.p2.hand:
            self.myDeck.discard.append(card)
        self.p2.clear()

    def repeatTrainAI(self):
        for x in xrange(0, 50):

            self.singleHandTraining()

    def trainAI(self):
        """AI plays with itself"""
        PERFECT_SCORE = 21

        while (True):
            p1_continue = continue_choice(self.p1) #does Player1 want to continue?
            p2_continue = continue_choice(self.p2) #does Player1 want to continue?

            if (self.p1.value > PERFECT_SCORE and self.p2.value > PERFECT_SCORE): #both players overdrew
                overdraft_correction(self.p1)
                overdraft_correction(self.p2)
            if (self.p1.value > PERFECT_SCORE): # P1 overdrew
                overdraft_correction(self.p1)
                declare_victory(self.p2)
                return    
            if (self.p2.value > PERFECT_SCORE): # P2 overdrew
                overdraft_correction(self.p2)
                declare_victory(self.p1)
                return  
            if (self.p1.value == PERFECT_SCORE): # P1 Blackjack
                declare_victory(self.p1)
                return
            if (self.p2.value == PERFECT_SCORE): # P2 BlackJack
                declare_victory(self.p2)
                return
            if (p1_continue == False and p2_continue == False): #no one wants to continue
                if (self.p1.value > self.p2.value):
                    underdraft_correction(self.p2)
                    declare_victory(self.p1)
                else:
                    underdraft_correction(self.p1)
                    declare_victory(self.p2)
                return
            if (p1_continue):
                playerDraw(self.p1, self.myDeck)
            if (p2_continue):
                playerDraw(self.p2, self.myDeck)
