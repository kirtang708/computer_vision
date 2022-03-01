# if below 800 there is no car and above 800 there is car

import cv2
import pickle
import cvzone
import numpy as np

#video feed 
cap = cv2.VideoCapture('carPark.mp4')

with open('carParkpos','rb') as f:
        posList = pickle.load(f) 

width, height = 107,48

def checkparkingspace(imgpro):

    spacecounter = 0

    for pos in posList:
        x,y = pos
        

        imgCrop = imgpro[y:y+height,x:x+width]   # in rectangle, car is available or not
        #cv2.imshow(str(x*y),imgCrop)  # each car separate image
        # count image pixel after more pixel is car and less pixel is empty space
        count = cv2.countNonZero(imgCrop) 
        # for text(number) in video
            #                            number location   big(size)                    
        
        if count <900:
            color = (0,255,0)
            thickness = 3
            spacecounter+= 1
        else:
            color = (0,0,255)
            thickness = 2

        
        
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,thickness)

        cvzone.putTextRect(img,str(count),(x,y+height-2),
                            scale=1, thickness=2, offset=0,colorR=color)    

        cvzone.putTextRect(img,f'Free: {spacecounter}/{len(posList)}',
                            (100, 55),scale=3, thickness=4, offset=20,colorR=(0,255,0))



while True:
    # for repeat video
    #  current frames                     total frames          
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)  # for repeat video
    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
     # for black and white
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,25,16)        
    
    imgMedium = cv2.medianBlur(imgThreshold,5) # for less dots (black and white)
    kernel = np.ones((3,3),np.uint8)
    imDilate = cv2.dilate(imgMedium,kernel, iterations=1)
    
    checkparkingspace(imDilate)
    
    
    
    

        
    cv2.imshow('video',img)
    #cv2.imshow('video_gray',imgGray)
    #cv2.imshow('video_gray',imgMedium)


    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    