#A list containing the values 2, 3, 4, 5, 6, 7, 8, 9, 10 and 11
valueList = {"2" : 4,
             "3" : 4,
             "4" : 4,
             "5" : 4,
             "6" : 4,
             "7" : 4,
             "8" : 4,
             "9" : 4,
             "10" : 16,
             "11" : 4}

hand = ["hq", "c2", "c8"]
handValue = 20
deckSize = 49
playerThreshold = 40

def updateList(card):
    value = 0

    if card[1] == 'k' or card[1] == 'q' or card[1] == 'j':
        value = 10
    elif card[1] == 'a':
        value = 11
    elif len(card) > 2:
        value = 10
    else:
        value = int(card[1])

    s1 = str(value)
    valueList[s1] -= 1

#updateList(hand)

#print valueList["10"]
#print valueList["2"]

def renewList():
    for x in xrange(2, 10):
        s = str(x)
        valueList[s] = 4
        print valueList[s]
    valueList["10"] = 16
    valueList["11"] = 4

def checkProbability(pHandValue, deckSize, threshold):
    Goal = 21
    leeway = Goal - pHandValue
    tempPercentage = 0.0
    for x in xrange(2, 11):
        if x <= leeway:
            s = str(x)
            tempPercentage += (float(valueList[s])/float(deckSize))
    tempPercentage += float(valueList["11"])/float(deckSize)
    tempPercentage *= 100.0
    print tempPercentage
    return tempPercentage >= threshold
#checkProbability(handValue, deckSize, playerThreshold)
#print checkProbability(handValue, deckSize, playerThreshold)

#renewList()
