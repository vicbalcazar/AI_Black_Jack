

#Bibliography: http://www.bicyclecards.com/how-to-play/blackjack/
# the use of this bibliography was liberal, there is no betting system and the deck resets after each round. Only the basic mechanics
#were simulated in this game.

import pygame, os, sys, random, time, AI, heuristic_AI1
pygame.init()
#HERE WE IMPORT AND TRAIN AI TO PLAY THE GAME
dealerAI = AI.BlackJack()
#Train AI, it will play 50 games with itself
dealerAI.repeatTrainAI()
decideAI = random.randint(1, 2)
print decideAI

#CHOOSE AI TO PLAY AGAINST
if decideAI == 1:
    if(dealerAI.p1.numOfWins > dealerAI.p2.numOfWins):
        opponent = dealerAI.p1
    else:
        opponent = dealerAI.p2
#else, it will use the heuristic AI with a threshold of 35, will will grab a card with 35% chance or higher
else:
    opponent = dealerAI.p1
threshold = 35



#DECK DEFINITIONS, INCLUDES A DECK AND A WAY TO SHUFFLE IT============================
"""Shuffles Deck"""
def shuffle(deck):
    """ Shuffles the deck using an implementation of the Fisher-Yates shuffling algorithm. n is equal to the length of the
    deck - 1 (because accessing lists starts at 0 instead of 1). While n is greater than 0, a random number k between 0
    and n is generated, and the card in the deck that is represented by the offset n is swapped with the card in the deck
    represented by the offset k. n is then decreased by 1, and the loop continues."""
        
    n = len(deck) - 1
    while n > 0:
        k = random.randint(0, n)
        deck[k], deck[n] = deck[n], deck[k]
        n -= 1

    return deck    
"""Initiates Deck"""
def createDeck():
    """ Creates a default deck which contains all 52 cards and returns it. This method was only slightly modified fromt he original source."""

    deck = ['sj', 'sq', 'sk', 'sa', 'hj', 'hq', 'hk', 'ha', 'cj', 'cq', 'ck', 'ca', 'dj', 'dq', 'dk', 'da']
    values = range(2,11)
    for x in values:
        spades = "s" + str(x)
        hearts = "h" + str(x)
        clubs = "c" + str(x)
        diamonds = "d" + str(x)
        deck.append(spades)
        deck.append(hearts)
        deck.append(clubs)
        deck.append(diamonds)
    return deck
#END OF DECK DEFINITIONS==============================================================

#THIS SECTION DEALS WITH THE FUNCTIONS THAT AFFECT THE PLAYERS' HANDS==================
"""Deals Hands"""
def initDeal(deck):
    """Deals the initial two hands to the player and the Brain(computer enemy)"""
    playerHand = []
    brainHand = []
    for x in xrange(0,2):
        playerHand.append(deck[0])
        del deck[0]
        brainHand.append(deck[0])
        del deck[0]
    return playerHand, brainHand, deck         
"""Def of the method which checks the value a hand: currently being worked on"""
def checkHandValue (hand):
    totalValue = 0
    stringVal = []
    aceInHand = False
    no_aces = 0
    for x in xrange(0, len(hand)):
        if len(hand[x]) <= 2:
            val = hand[x][1]
            if hand[x][1] == 'a':
                aceInHand = True
        else:
            val = hand[x][1] + hand[x][2]
        stringVal.append(val)

    for x in xrange(0, len(stringVal)):
        if stringVal[x] == 'k' or stringVal[x] == 'q'or stringVal[x] == 'j':
            totalValue += 10
        elif stringVal[x] == 'a':
            totalValue += 11
            no_aces += 1
        else:
            totalValue += int(stringVal[x])
    if totalValue > 21 and aceInHand:
        totalValue -= 10
    opponent.aces = no_aces

    return totalValue
"""Gives the card atop of the deck to the designated player"""
def hitHand(hand, deck):
    hand.append(deck[0])
    del deck[0]
    return hand
#END OF FUNCTIONS THAT AFFECT THE PLAYERS' HANDS=======================================

#Definitions for displaying player hand, and a seperate one for brain hand=============
"""display player Hand"""
def displayPHand (playerHand):
    pixels = 80 #amount of pixels to move card
    for x in xrange (0, len(playerHand)):
        gameDisplay.blit(pygame.image.load('images/' + playerHand[x] + '.png'), ((pixels*(x)),490))
    """Player Hand Disply done"""
"""Brain Hand display Definition"""
def displayBHand (brainHand, EndOfRound):
    pixels = 80
    
    if EndOfRound:
        for x in xrange (0, len(brainHand)):
            gameDisplay.blit(pygame.image.load('images/' + brainHand[x] + '.png'), ((pixels*(x)),0))
    elif EndOfRound == False:
        gameDisplay.blit(pygame.image.load('images/back.png'), (0,0))
        for x in xrange (1, len(brainHand)):
            gameDisplay.blit(pygame.image.load('images/' + brainHand[x] + '.png'), ((pixels*(x)),0))
#END===================================================================================

#FUNCTIONS THAT CHECK THE STATE OF THE GAME(TECHNICALLY)===============================
"""Checks if either or both players got BlackJack"""
def checkBlackJack(pHandValue, bHandValue):
    if pHandValue == 21 and bHandValue == 21:
        return "tie blackjack"
    elif pHandValue == 21 and bHandValue != 21:
        return "player win blackjack"
    elif pHandValue != 21 and bHandValue == 21:
        return "brain win blackjack"
    return "no"
"""Checks if either player goes over 21 and loses"""
def checkIfBust(pHandValue, bHandValue):
    if pHandValue > 21 and bHandValue < 21:
        return "player bust"
    elif bHandValue > 21 and pHandValue < 21:
        return "brain bust" 
    else:
        return "no"
"""Checks who got the most hand value at the end of the round"""
def checkWhoWon (pHandValue, bHandValue):
    if pHandValue == bHandValue and pHandValue <= 21:
        return "tie"
    elif pHandValue > bHandValue and pHandValue <= 21:
        return "player win"
    else:
        return "brain win"
"""When Called this resets everything to their initial states"""
def reset(initialState, endOfRound, pHand, bHand, pHandVal, bHandVal):
    pHand = []
    bHand = []
    pHandVal = 0
    bHandVal = 0
    initialState = True
    endOfRound = False
    return initialState, endOfRound, pHand, bHand, pHandVal, bHandVal
#END OF FUNCTIONS THAT CHECK STATE OF THE GAME========================================

#SYSTEM FUNCTIONS(WELL FUNCTION IN THIS CASE)=========================================
"""General purpose function to display text to screen"""
def displayMsgToScreen(msg, color, x, y):
    screenText = font.render(msg, True, color)
    gameDisplay.blit(screenText, [x, y])
#END OF SYSTEM FUNCTION================================================================
#INITIALIZATION - Here I create most of the variables that need to be initialized first so python doesn't freak out
green = (0,255,0)
black = (0, 0, 0)
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('BlackJack')

testDeck = []
playerHand = []
brainHand = []
playerHandValue = 0
brainHandValue = 0
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()
"""Here is where I put all my Boolean logic, big fan of it"""
done = False
EndOfRound = False
initialState = True
#Reset = False
#END OF INITIALIZATION=====================================================

#MAIN GAME LOOP=============================================================================
while not done:
    gameDisplay.fill((green))
 
    #Determines if it should display the hand
    if initialState == False:
        displayPHand(playerHand)
        displayBHand(brainHand,EndOfRound)
        
    #This Block Checks if someone got BlackJack==============================================
    if checkBlackJack(playerHandValue, brainHandValue) == "tie blackjack" :
        xPos = 280
        yPos = 275
        displayMsgToScreen("You both got Blackjack and tied", black, xPos, yPos)
        EndOfRound = True
        
    elif checkBlackJack(playerHandValue, brainHandValue) == "player win blackjack" :
        xPos = 280
        yPos = 275
        EndOfRound = True
        displayMsgToScreen("You got Blackjack!!!", black, xPos, yPos)
        
    elif checkBlackJack(playerHandValue, brainHandValue) == "brain win blackjack" :
        xPos = 280
        yPos = 275
        EndOfRound = True
        displayMsgToScreen("Brain got Blackjack!!!", black, xPos, yPos)
        
    # END of Block that Checks if someone got BlackJack======================================

    #This Block Checks if someone got Bust===================================================
    if checkIfBust(playerHandValue,brainHandValue) == "player bust" :
        xPos = 280
        yPos = 275
        EndOfRound = True
        displayMsgToScreen("You Busted!!! You Lose!!!", black, xPos, yPos)
    elif checkIfBust(playerHandValue,brainHandValue) == "brain bust" :
        xPos = 280
        yPos = 275
        EndOfRound = True
        displayMsgToScreen("Brain Busted!!! You Win !!!", black, xPos, yPos)

    #END of BUST BLOCK=======================================================================

    #Block that Checks Who Won after player decides to stay and hasn't busted or gotten BlackJack
    if checkWhoWon(playerHandValue,brainHandValue) == "tie" and EndOfRound and checkIfBust(playerHandValue,brainHandValue) == "no" and checkBlackJack(playerHandValue, brainHandValue) == "no":
        xPos = 280
        yPos = 275
        
        displayMsgToScreen("You Both Tied!!!", black, xPos, yPos)
    elif checkWhoWon(playerHandValue,brainHandValue) == "player win" and EndOfRound and checkIfBust(playerHandValue,brainHandValue) == "no" and checkBlackJack(playerHandValue, brainHandValue) == "no":
        xPos = 280
        yPos = 275
        
        displayMsgToScreen("You Won!!!", black, xPos, yPos)
    elif checkWhoWon(playerHandValue,brainHandValue) == "brain win" and EndOfRound and checkIfBust(playerHandValue,brainHandValue) == "no" and checkBlackJack(playerHandValue, brainHandValue) == "no":
        xPos = 280
        yPos = 275
        #print "fuck me"
        displayMsgToScreen("You Lose!!!", black, xPos, yPos)
    #END of CHeck who won Block==============================================================

    #Block that displays messages to signify game state======================================
    playerHandValue = checkHandValue(playerHand)
    brainHandValue = checkHandValue(brainHand)
    opponent.value = checkHandValue(brainHand)
    if initialState:
        xPos = 280
        yPos = 275
        displayMsgToScreen("Press the d key to deal hands", black, xPos, yPos)

    if initialState == False and EndOfRound == False:
        xPos = 280
        yPos = 275
        yPos2 = 301
        displayMsgToScreen("Press the space bar to hit", black, xPos, yPos)
        displayMsgToScreen("Press the s key to stay", black, xPos, yPos2)

    if EndOfRound:
        xPos = 280
        yPos2 = 300
        displayMsgToScreen("Press the Enter key to play again", black, xPos, yPos2)
        heuristic_AI1.renewList()
    #END of Block that displays game State ==================================================
    
    #KeyPress Controls===============================================================================
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and initialState == False and EndOfRound == False:
            #showR = not showR
            hitHand(playerHand, testDeck)
            #if brainHandValue < 17:
            if decideAI == 1:
                if AI.continue_choice(opponent):
                    hitHand(brainHand, testDeck) 
            elif (heuristic_AI1.checkProbability(brainHandValue, len(testDeck), threshold)):
                hitHand(brainHand, testDeck)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d and initialState:
            initialState = False
            testDeck = createDeck()
            shuffle(testDeck)
            playerHand, brainHand, testDeck = initDeal(testDeck)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and initialState == False:
            EndOfRound = True
            #if brainHandValue < 17:
            if decideAI == 1:
                if AI.continue_choice(opponent):
                    hitHand(brainHand, testDeck) 
            elif (heuristic_AI1.checkProbability(brainHandValue, len(testDeck), threshold)):
                hitHand(brainHand, testDeck)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and initialState == False and EndOfRound:
            initialState, EndOfRound, playerHand, brainHand, playerHandValue, brainHandValue = reset(initialState, EndOfRound, playerHand, brainHand, playerHandValue, brainHandValue)

        if event.type == pygame.QUIT:
            done = True
   
    

    pygame.display.flip()
    clock.tick(60)
#END OF MAIN GAME LOOP==============================================================================================================
pygame.quit()
quit()