
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



#####################################
wCam, hCam = 640,480
#####################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar= 400
volper = 0



while True:
    success, img = cap.read()
    
    # find hand
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    
    
    if len(lmlist) !=0:
        
        # filter based on size      
        # find distance between index and thumb 
        # convert volume
        # reduce resolution to make it smoother 
        # check finger up 
        # if pinky is down set volume
        # frame rate
        
        
        # detect only 4(thumb) & 8(index finger) 
        #print(lmlist[4],lmlist[8]) 
        
        x1, y1 = lmlist[4][1], lmlist[4][2] # first element is X[4][1] and second element is Y[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        
        
        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255),3)
        cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)
        
        length = math.hypot(x2-x1, y2-y1)  # hypot means squre root 
        print(length) 
        
        # hand Range 50 -> 180
        #volume Range -65 -> 0
        # sensitivity
        
        vol = np.interp(length, [50, 180], [minVol, maxVol])
        volBar = np.interp(length, [50, 180], [400, 150])
        volper = np.interp(length, [50, 180], [0, 100])        
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol,None)
        
        # two finger between length less than 50 then, middle circle color changed (green)
        if length<50:
            cv2.circle(img, (cx,cy), 10, (0,255,0), cv2.FILLED)
            
            
    cv2.rectangle(img, (40,130), (85,400),(0,255,0),2)   
    cv2.rectangle(img, (40,int(volBar)), (85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volper)}%',(40,450), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0), 2)
          
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 
    
    cv2.putText(img,f'FPS:{int(fps)}',(15,25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0), 2)
    
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    