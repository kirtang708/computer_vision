
import cv2
import math

path = '1.jpg'
img = cv2.imread(path)
pointsList = []

# when i click and output are give location of mine click
def mousePoint(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # when i click then draw the circle and give value of x and y
        cv2.circle(img,(x,y),5,(0,0,255),cv2.FILLED) 
        pointsList.append([x,y]) # for save in pointList
        print(pointsList)
        

while True:
    cv2.imshow('image',img)
    cv2.setMouseCallback('image',mousePoint)
    
    # WHEN I PRESS 'C' THEN MY ALL CHECK POINT ARE REMOVE AND 
    #  OPEN NEW IMAGE
    if cv2.waitKey(1) & 0xFF == ord('c'):
        pointsList = []
        img = cv2.imread(path)