import random


class Deck:
    """A simple Deck class. It initializes the deck. It allows for drawing, keeping track of discarded cards and can be printed out"""
    deck = []
    discard = []

    def __init__(self):
        self.deck = ['sj', 'sq', 'sk', 'sa', 'hj', 'hq', 'hk', 'ha', 'cj', 'cq', 'ck', 'ca', 'dj', 'dq', 'dk', 'da']
        values = range(2, 11) 
        for i in values:
            spades = "s" + str(i)
            hearts = "h" + str(i)
            clubs = "c" + str(i)
            diamonds = "d" + str(i)
            self.deck.append(spades)
            self.deck.append(hearts)
            self.deck.append(clubs)
            self.deck.append(diamonds)
        #shuffle the deck
        n = len(self.deck) - 1
        while n > 0:
            k = random.randint(0, n)
            self.deck[k], self.deck[n] = self.deck[n], self.deck[k]
            n -= 1
	    
    def __str__(self):
        s = ""
        for c in self.deck:
            s += c + "\n"
        return s

    
    def peek(self):
        return self.deck[0]
    """Returns the first card from the deck's 'top' and it removes it from the list as well"""
    def draw(self):
        card = self.deck[0]
        #self.discard.append(deck[0])
        del self.deck[0]
        return card
    """INPUT: a 'hand', it can be passed as a list. It adds the cards from the hand to the discard pile. The actual deletion of the
    hand is handled elsewhere."""
    def discardHand(self, hand):
        for c in hand:
            self.discard.append(c)
    """Function shuffles the deck"""
    def shuffle(self):
        n = len(self.deck) - 1
        while n > 0:
            k = random.randint(0, n)
            self.deck[k], self.deck[n] = self.deck[n], self.deck[k]
            n -= 1
    """Reshuffles the deck after it appends the discard pile at the end. It also empties the discard pile"""
    def renew(self):
        for i in self.discard:
            self.deck.append(i)
        self.discard = []
        self.shuffle()

    def size(self):
        return len(self.deck)