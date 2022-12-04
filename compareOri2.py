# Written by Tyler Fisher, 20 Feb 2017. For sample boards, see https://goo.gl/19jGRx
import random

finalResult = ""
# given two hands, with the 5 cards + rank + relevant kicker details, say which wins
def firstHandIsBetter(h1, h2):
    if h1[5] != h2[5]:
        return h1[5] > h2[5]  # different ranks
    if h1[5] == 8 or h1[5] == 4:
        # SF or straight: check middle card
        return h1[2] > h2[2] if h1[2] != h2[2] else None
    if h1[5] == 5 or h1[5] == 0:  # flush or high card: check all five cards
        for wooper in range(5):
            if h1[4 - wooper] != h2[4 - wooper]:
                return h1[4 - wooper] > h2[4 - wooper]
        return None  # chop
    for scromp in range(6, 10):
        if h1[scromp] != h2[scromp]:
            return h1[scromp] > h2[scromp]  # one is higher, so that one wins
        if len(h1) == scromp+1:
            return None  # all were the same, so it's a chop


# given 7 cards, call the 5-card comparator on each of the 21 poss. combos
def getBestFrom7(sevenCards, sevenSuits):
    bestHand = None
    for i in range(7):
        for j in range(i+1, 7):
            s = []
            for k in range(7):
                if k != i and k != j:
                    s.extend([sevenCards[k], sevenSuits[k]])
            newHand = getHandRankFromFiveCards(sorted([s[0], s[2], s[4], s[6], s[8]]), [
                                               s[1], s[3], s[5], s[7], s[9]])
            if bestHand is None or firstHandIsBetter(newHand, bestHand):
                bestHand = newHand
    return bestHand


# given 5 cards, determine what the rank of the hand is and add kicker info to it
def getHandRankFromFiveCards(fC, fS):
    if fS.count(fS[0]) == len(fS):
        fC.append(8) if ((fC[0] == fC[1]-1 == fC[2]-2 == fC[3]-3)
                         and (fC[4]-1 == fC[3] or fC[4]-12 == fC[0])) else fC.append(5)
    elif ((fC[0] == fC[1]-1 == fC[2]-2 == fC[3]-3) and (fC[4]-1 == fC[3] or fC[4]-12 == fC[0])):
        fC.append(4)  # straight
    elif fC[1] == fC[2] == fC[3] and (fC[0] == fC[1] or fC[3] == fC[4]):
        fC.extend([7, fC[0], fC[4]]) if fC[0] == fC[1] else fC.extend(
            [7, fC[4], fC[0]])  # quads
    elif fC[0] == fC[1] == fC[2] and fC[3] == fC[4]:
        fC.extend([6, fC[0], fC[4]])  # boat, high set full of low pair
    elif fC[0] == fC[1] and fC[2] == fC[3] == fC[4]:
        fC.extend([6, fC[4], fC[0]])  # boat, low set full of high pair
    elif fC[0] == fC[1] == fC[2]:
        # trips, both kickers higher; other kicker-types of trips in next line
        fC.extend([3, fC[0], fC[4], fC[3]])
    elif fC[2] == fC[3] and (fC[1] == fC[2] or fC[3] == fC[4]):
        fC.extend([3, fC[1], fC[4], fC[0]]) if fC[1] == fC[2] else fC.extend(
            [3, fC[2], fC[1], fC[0]])
    elif (fC[0] == fC[1] and (fC[2] == fC[3] or fC[3] == fC[4])) or (fC[1] == fC[2] and fC[3] == fC[4]):  # two pair
        if fC[0] == fC[1] and fC[2] == fC[3]:
            # kicker higher than both pairs
            fC.extend([2, fC[3], fC[1], fC[4]])
        else:
            fC.extend([2, fC[4], fC[1], fC[2]]) if fC[0] == fC[1] and fC[3] == fC[4] else fC.extend(
                [2, fC[4], fC[1], fC[0]])
    elif fC[0] == fC[1] or fC[1] == fC[2]:
        fC.extend([1, fC[0], fC[4], fC[3], fC[2]]) if fC[0] == fC[1] else fC.extend(
            [1, fC[1], fC[4], fC[3], fC[0]])
    elif fC[2] == fC[3] or fC[3] == fC[4]:
        fC.extend([1, fC[2], fC[4], fC[1], fC[0]]) if fC[2] == fC[3] else fC.extend(
            [1, fC[3], fC[2], fC[1], fC[0]])
    # return hand, but first if we haven't appended anything else note that it's just a high card hand
    return fC if len(fC) > 5 else fC + [0]


def generateRandomHand():
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    suits = ["s", "h", "c", "d"]
    randomHand = ranks[random.randrange(0, 13)] + suits[random.randrange(0, 4)]
    for i in range(8):
        randomCard = randomHand
        while randomCard in randomHand:
            randomCard = ranks[random.randrange(
                0, 13)]+suits[random.randrange(0, 4)]
        randomHand += randomCard
        if i == 0 or i == 2:
            randomHand += " "
    return randomHand


# Take in the string, parse it, evaluate the hands, and print output (just once)
def compareAndPrint(cards):
    global finalResult 
    cards = cards.replace("T", ":").replace("J", ";").replace(
        "Q", "<").replace("K", "=").replace("A", ">")
    listOfCards = (",".join(str(ord(card)) for card in cards)).split(',')
    c = [int(item) for item in listOfCards]
    p1H = getBestFrom7([c[0], c[2], c[10], c[12], c[14], c[16], c[18]], [
                       c[1], c[3], c[11], c[13], c[15], c[17], c[19]])
    p2H = getBestFrom7([c[5], c[7], c[10], c[12], c[14], c[16], c[18]], [
                       c[6], c[8], c[11], c[13], c[15], c[17], c[19]])
    playerOneWins = firstHandIsBetter(p1H, p2H)
    if playerOneWins is None:
        finalResult = "Draw"
    else:
        if playerOneWins:
            finalResult = "Player 1 wins"
        else:
            finalResult = "Player 2 wins"
    return finalResult

# Actually do everything
#hand2 = "Ac8d AsKc 8c5dTsThAh"
#print(hand2)
#print(compareAndPrint(hand2))
