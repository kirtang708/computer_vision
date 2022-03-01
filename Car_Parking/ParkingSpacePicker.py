import cv2
import pickle



            # 157-50, 240-192 
width, height = 107,48

try:                               
    with open('carParkpos','rb') as f:
        posList = pickle.load(f)   # pickle no upyog car parking box jadvi rakhva 
except:
    posList = []    


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:  
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)



    with open('carParkpos','wb') as f:  # car parking box not invisible when code restart
        pickle.dump(posList, f)




while True:
    img = cv2.imread('carParking.png')
    for pos in posList:
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)


    cv2.imshow('Image',img)
    cv2.setMouseCallback('Image',mouseClick)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
