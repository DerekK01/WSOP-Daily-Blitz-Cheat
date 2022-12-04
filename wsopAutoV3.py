

from queue import Empty
import matplotlib.pyplot as plt
from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np
from compareOri2 import compareAndPrint
import pyautogui
import time
import mss


#Identify the number of each card
def getCard(imageGray):
    result = ""
    cardNumber=['A','2','3','4','5','6','7','8','9','T','J','K','Q']
    for i in cardNumber:
        template = cv.imread('Number/' + i + '.jpg', 0)
        result = matching(imageGray,template)
        if result == "Match":
            result = "Match"
            out = i
            break
    if result != "Match":
        #print("None")
        out = None
    return out

#Identify the symbol of each card
def getSymbol(imageGray):
    result = ""
    cardSymbol=['c','d','h','s']
    for i in cardSymbol:
        template = cv.imread('Number/' + i + '.jpg', 0)
        result = matching(imageGray,template)
        if result == "Match":
            result = "Match"
            #print(i)
            out = i
            break
    if result != "Match":
        #print("None")
        out = None
    return out

#Matching the given image to the template
def matching(imageGray,templateGray):

    # Store width and height of template in w and h
    w, h = templateGray.shape[::-1]
    
    # Perform match operations.
    res = cv.matchTemplate(imageGray, templateGray, cv.TM_CCOEFF_NORMED)
    
    # Specify a threshold
    threshold = 0.9
    
    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)
    if loc[0].size == 0:
        result = "No match"
    else:
        result = "Match"
    #print(result)
    return result


#Scan the screen and grap all the number and symbol 
def scan():
    screen = Image.open("test.png")
    with mss.mss() as sct:
    # Grab the data
        first = sct.grab((456, 299, 456+75, 299+110))
        second = sct.grab((661, 299, 661+75, 299+110))
        first = cv.cvtColor(np.array(first), cv.COLOR_RGB2GRAY)
        second = cv.cvtColor(np.array(second), cv.COLOR_RGB2GRAY)
        if getCard(first) == None or getCard(second) == None:
            return None
        third = sct.grab((861, 299, 861+75, 299+110))
        fourth = sct.grab((1062, 299, 1062+75, 299+110))
        fifth = sct.grab((1266, 299, 1266+75, 299+110))


        hand1 = sct.grab((556, 615, 556+75, 615+110))
        hand1_r = sct.grab((441, 615, 441+80, 615+120))


        hand2 = sct.grab((1168, 615, 1168+75, 615+110))
        hand2_r = sct.grab((1270, 605, 1270+75, 605+110))

        first_i = sct.grab((456, 401, 456+60, 401+110))
        second_i = sct.grab((657, 401, 657+60, 401+110))
        third_i = sct.grab((861, 401, 861+60, 401+110))
        fourth_i = sct.grab((1062, 401, 1062+60, 401+110))
        fifth_i = sct.grab((1266, 401, 1266+60, 401+110))

        hand1_i = sct.grab((556, 719, 556+60, 719+100))
        hand1_r_i = sct.grab((457, 732, 457+70, 732+100))

        hand2_i = sct.grab((1168, 716, 1168+60, 716+100))
        hand2_r_i = sct.grab((1257, 710, 1257+60, 710+100))


    third = cv.cvtColor(np.array(third), cv.COLOR_RGB2GRAY)
    fourth = cv.cvtColor(np.array(fourth), cv.COLOR_RGB2GRAY)
    fifth = cv.cvtColor(np.array(fifth), cv.COLOR_RGB2GRAY)

    hand1_r = cv.cvtColor(np.array(hand1_r), cv.COLOR_RGB2GRAY)
    hand1 = cv.cvtColor(np.array(hand1), cv.COLOR_RGB2GRAY)

    hand2 = cv.cvtColor(np.array(hand2), cv.COLOR_RGB2GRAY)
    hand2_r = cv.cvtColor(np.array(hand2_r), cv.COLOR_RGB2GRAY)

    #for hand1_r rotate -4 degree
    rows,cols= hand1_r.shape 
    M = cv.getRotationMatrix2D((cols/2,rows/2),-8,1) 
    hand1_r = cv.warpAffine(hand1_r,M,(cols,rows)) 

    #for hand2_r rotate 4 degree
    rows,cols= hand2_r.shape 
    M = cv.getRotationMatrix2D((cols/2,rows/2),8,1) 
    hand2_r = cv.warpAffine(hand2_r,M,(cols,rows)) 



    first_i = cv.cvtColor(np.array(first_i), cv.COLOR_RGB2GRAY)
    second_i = cv.cvtColor(np.array(second_i), cv.COLOR_RGB2GRAY)
    third_i = cv.cvtColor(np.array(third_i), cv.COLOR_RGB2GRAY)
    fourth_i = cv.cvtColor(np.array(fourth_i), cv.COLOR_RGB2GRAY)
    fifth_i = cv.cvtColor(np.array(fifth_i), cv.COLOR_RGB2GRAY)

    hand1_r_i = cv.cvtColor(np.array(hand1_r_i), cv.COLOR_RGB2GRAY)
    hand1_i = cv.cvtColor(np.array(hand1_i), cv.COLOR_RGB2GRAY)

    hand2_i = cv.cvtColor(np.array(hand2_i), cv.COLOR_RGB2GRAY)
    hand2_r_i = cv.cvtColor(np.array(hand2_r_i), cv.COLOR_RGB2GRAY)

    #for hand1_r rotate -4 degree
    rows,cols= hand1_r_i.shape 
    M = cv.getRotationMatrix2D((cols/2,rows/2),-8,1) 
    hand1_r_i = cv.warpAffine(hand1_r_i,M,(cols,rows)) 

    #for hand2_r rotate 4 degree
    rows,cols= hand2_r_i.shape 
    M = cv.getRotationMatrix2D((cols/2,rows/2),8,1) 
    hand2_r_i = cv.warpAffine(hand2_r_i,M,(cols,rows)) 

    dealerCard = [first,second,third,fourth,fifth]
    dealerCard_i = [first_i,second_i,third_i,fourth_i,fifth_i]
    p1 = [hand1_r,hand1]
    p2 = [hand2,hand2_r]
    p1_i = [hand1_r_i,hand1_i]
    p2_i = [hand2_i,hand2_r_i]

    return dealerCard,dealerCard_i,p1,p2,p1_i,p2_i



#Stopping the loop if it doesn't detect an valid card. This allow the software to have a faster respond time.
def main():
    global count
    global lastRecord
    current = ""
    try:
        dealerCard,dealerCard_i,p1,p2,p1_i,p2_i = scan()
    except:
        return

    stop = False

    for i in range(0,2):
        num = getCard(p1[i])
        if num == None:
            stop = True
            break
        if num != None:
            sym = getSymbol(p1_i[i])
            if sym != None:
                current += num
                current += sym
            else:
                stop = True
                break

    if stop == False:
        current += " "
        for i in range(0,2):
            num = getCard(p2[i])
            if num == None:
                stop = True
                break
            if num != None:
                sym = getSymbol(p2_i[i])
                if sym != None:
                    current += num
                    current += sym
                else:
                    stop = True
                    break
    if stop == False:
        current += " "
        for i in range(0,5):
            num = getCard(dealerCard[i])
            if num == None:
                stop = True
                #print(i)
                break
            if num != None:
                sym = getSymbol(dealerCard_i[i])
                if sym != None:
                    current += num
                    current += sym
                else:
                    stop = True
                    break

    
    if stop == False and lastRecord != current:
        count += 1
        #compare the poker hand
        winner = compareAndPrint(current)
        if winner == "Player 2 wins":
            pyautogui.click(1321, 719)
        elif winner == "Player 1 wins":
            pyautogui.click(680, 729)
        else:
            pyautogui.click(680, 729)
        print(current)

        lastRecord=current

#TESTING / DEBUG
#==============================================
#Testing the degree rotation for the card on the side
def testDegree(image,template):
    rows,cols= image.shape
    for i in range (1,360):
        result = matching(image,template)
        if result != "Match":
            M = cv.getRotationMatrix2D((cols/2,rows/2),i,1) 
            image = cv.warpAffine(image,M,(cols,rows))  
        else:
            print("found")
            print(i)
            cv.imshow('test',image)
            cv.waitKey(0)   

def test():
    dealerCard,dealerCard_i,p1,p2,p1_i,p2_i = scan()
    for i in range(0,5):
        cv.imshow('test',dealerCard[i])
        cv.waitKey(0)
        print(getCard(dealerCard[i]))
    for i in range(0,5):
        cv.imshow('test',dealerCard_i[i])
        cv.waitKey(0)
        print(getSymbol(dealerCard_i[i]))

    for i in range(0,2):
        cv.imshow('test',p1[i])
        cv.waitKey(0)
        print(getCard(p1[i]))
    for i in range(0,2):
        cv.imshow('test',p1_i[i])
        cv.waitKey(0)
        print(getSymbol(p1_i[i]))

    for i in range(0,2):
        cv.imshow('test',p2[i])
        cv.waitKey(0)
        print(getCard(p2[i]))
    for i in range(0,2):
        cv.imshow('test',p2_i[i])
        cv.waitKey(0)
        print(getSymbol(p2_i[i]))
#==============================================


#SETUP
#==============================================
print("START")
count = 0
lastRecord = ""
#==============================================


#TESTING / DEBUG
#==============================================
#test()
#dealerCard,dealerCard_i,p1,p2,p1_i,p2_i = scan()
#template = cv.imread('Number/7.jpg', 0)
#print(matching(p1[0],template))
#print(getCard(p1[0]))
# template = cv.imread('Number/7.jpg', 0)
# testDegree(p1[0],template)
#==============================================


while(True):
   main()
#main()
