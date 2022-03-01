
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
# for connect system volume to code
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

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

# connect system volume to code
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
area = 0
colorvol = (0,255,0) # for color change purpose


while True:
    success, img = cap.read()
    
    # find hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)
    
    
    if len(lmList) !=0:
        
        # filter based on size
             
        # find distance between index and thumb
        area= (bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100 
        # print(area)
        if 150 <area<1000:
            # print('YES')
        # find distance between index and thumb
            length, img, lineinfo = detector.findDistance(4,8,img) # 4-> thumb & 8 -> index finger
            # print(length)
            
            
        # convert volume
         
            
            volBar = np.interp(length, [50, 200], [400, 150])
            volper = np.interp(length, [50, 200], [0, 100])        
           
            
            # reduce resolution to make it smoother 
            smoothness = 5
            volper = smoothness * round(volper/smoothness)  # round means round figure
            
            # check finger up 
            fingers = detector.fingersup()
            print(fingers)
            
            # if pinky is down set volume
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volper/100,None)
                cv2.circle(img, (lineinfo[4],lineinfo[5]), 10, (0,255,0), cv2.FILLED)
                
                # when volume set color are change 
                colorvol = (255,0,0)
            else:
                colorvol = (0,255,0)
                    
           
            
    cv2.rectangle(img, (40,130), (85,400),(0,255,0),2)   
    cv2.rectangle(img, (40,int(volBar)), (85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volper)}%',(40,450), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0), 2)
    cvol = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(img,f'Vol Set:{int(cvol)}',(500,25), cv2.FONT_HERSHEY_PLAIN, 1.5, colorvol, 2)
     
                
                
    # frame rate        
        
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 
    
    cv2.putText(img,f'FPS:{int(fps)}',(15,25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0), 2)
    
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    