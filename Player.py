class Player:
    hand = []
    value = 0
    image = []
    name = ""
    numOfWins = 0

    def __init__(self, name, th):
        self.name = name
        self.threshold = th
        self.wins = 0
        self.value = 0
        self.aces = 0
        self.hand = []
        self.image = []
        self.blackjack = False
        

    def checkValue(self):
        tempValue = 0
        for card in self.hand:
            if card[1] == 'k' or card[1] == 'q' or card[1] == 'j':
                tempValue += 10
            elif card[1] == 'a':
                tempValue += 11
                self.aces += 1
                if tempValue > 21:
                    tempValue -= 10
            elif len(card) > 2: 
                tempValue += 10
            else:
                tempValue += int(card[1])

        self.value = tempValue
        return self.value

    def size(self):
        return len(self.hand)

    def __str__ (self):
        #checkValue()
        s = ""
        for card in self.hand:
            s += card + ", "

        s += " value of hand: " + str(self.checkValue())

        return self.name + " hand: " + s

    def addCard(self, card):
        self.hand.append(card)
        self.value = self.checkValue()

    def clear(self):
        self.hand = []
        self.image = []
        self.value = 0
        self.aces = 0
        self.blackjack = False

    def wins(self):
        return self.numOfWins