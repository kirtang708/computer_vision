
import cv2
import math
import mediapipe as mp
import time
class handDetector():
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)                
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax 
            
            if draw:
                cv2.rectangle(img, (bbox[0]-20,bbox[1]-20),(bbox[2]+20,bbox[3]+20), (0,255,0),2) # 20 (+&-) bounding box size maate   
            
        return self.lmList, bbox
    
    
    def fingersup(self):
        fingers = []
        
        # thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # 4 finger
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    
    
    def findDistance(self, p1, p2, img, draw=True):
              # detect only 4(thumb) & 8(index finger) 
        #print(lmlist[4],lmlist[8]) 
        
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2] # first element is X[4][1] and second element is Y[4][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        
        if draw:
            cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (255,0,255),3)
            cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)
            
        length = math.hypot(x2-x1, y2-y1)  # hypot means squre root
        return length, img, [x1,y1,x2,y2,cx,cy]
    
    
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[0])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    
if __name__ == "__main__":
    main()