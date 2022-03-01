import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm


###################################
brushthickness = 15
eraserthickness = 100
##################################

folderpath = 'header'
myList = os.listdir(folderpath)
#print(myList)
overlayList = []

for impath in myList:
    image = cv2.imread(f'{folderpath}/{impath}')
    overlayList.append(image)
#print(len(overlayList))
header = overlayList[0]
drawcolor = (255,0,255)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0 # x previous and y previous
imgcanvas = np.zeros((720,1280,3), np.uint8)  #new image create

while True:
    
    # 1. import image
    success, img = cap.read()
    img = cv2.flip(img, 1) # because fs i scroll my hand right side then go right not opposite direction 
    
    # 2. find handlandmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False) # lmlist = landmark list
    
    if len(lmList)!= 0:
        #print(lmlist)
        
        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]  # 8 is 1st finger 
        x2, y2 = lmList[12][1:]  #12 is middle finger
    
    
        # 3. check which fingers are up
        
        fingers = detector.fingersup()
        #print(fingers)
        
        # 4. if selection mode - Two fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print('selection mode')
            # checking for click
            if y1 < 125:
                if 200<x1<450:
                    header = overlayList[0]
                    drawcolor = (255,0,255)
            
                if 500<x1<650:
                    header = overlayList[1]
                    drawcolor = (255,0,0)
            
                if 700<x1<950:
                    header = overlayList[2]
                    drawcolor = (0,255,0)
            
                if 1050<x1<1280:
                    header = overlayList[3]
                    drawcolor = (0,0,0)
                    
            cv2.rectangle(img, (x1,y1-25),(x2,y2+25), drawcolor,cv2.FILLED)
            
        
        # 5. if drawing modce - index finger is up
        
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1,y1),15, drawcolor,cv2.FILLED)
            print('drawing mode')
            if xp==0 and yp == 0:
                xp, yp =x1,y1 
                
            if drawcolor == (0,0,0):
                cv2.line(img, (xp,yp),(x1,y1),drawcolor,eraserthickness)
                cv2.line(imgcanvas, (xp,yp),(x1,y1),drawcolor,eraserthickness)
            else:
                cv2.line(img, (xp,yp),(x1,y1),drawcolor,brushthickness)
                cv2.line(imgcanvas, (xp,yp),(x1,y1),drawcolor,brushthickness)
        
            xp, yp = x1, y1
            
    imggray = cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imggray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img, imgcanvas)
    
    # setting the header image
    img[0:125,0:1280] = header
    # img = cv2.addWeighted(img,0.5,imgcanvas,0.5,0)
    cv2.imshow('image',img)
    cv2.imshow('canvas',imgcanvas)
    cv2.imshow('canvas',imgInv)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break