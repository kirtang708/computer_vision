import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()  # dots
mpDraw = mp.solutions.drawing_utils  # small dots on hands

pTime = 0      # previous time
cTime = 0      # current time


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # for conver image
    results = hands.process(imgRGB)   # that will proccess frame for us 
    #print(results.multi_hand_landmarks)  # something detected or not

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):        # enumerate = calculation
                #print(id, lm)
                h, w, c = img.shape    # height, width, channel os image
                cx, cy =int(lm.x*w), int(lm.y*h)  # landmark.x*width & landmark.y*height   
                print(id, cx, cy)
                if id == 4:  # dark for only circle for thumb
                    cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)   # radius = 5 and this is for thumb circle
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)  # hand connection is connect points
            

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
                #print integer      between 1 to 70   font style    width=1.5    color=purple    thickness=2 
    cv2.putText(img, str(int(fps)), (10,40), cv2.FONT_HERSHEY_PLAIN,2,(0, 255, 0),2)      
    
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    
