import Module as m
import cv2
import math

cap = cv2.VideoCapture(0)
detector = m.handDetector()

lid={ #Landmark ID
    "W": 0,
    #Fingertips
    "TTip": 4,
    "ITip": 8,
    "MTip": 12,
    "RTip": 16,
    "PTip": 20,
    #pips
    "TPip": 2,
    "IPip": 6,
    "MPip": 10,
    "RPip": 14,
    "PPip": 18,
    

}

x, y = 1,2


while True:
    success, img = cap.read()

    img = detector.findHands(img)

    landmarks = detector.getPositions()
    if len(landmarks) != 0: # Dubbelkollar att den faktiskt hittar en eller flera händer

        #Tummen upp
        '''if all(i[y] >= landmarks[0][lid["TTip"]][y] for i in (landmarks[0][::4])):
            print("Thumbs up")
        else:
            print("NO")'''
        
        # abs(landmarks[0][lid["ITip"]][y] - landmarks[0][lid["IPip"]][y]) > moe

        moe = 0.75 #Margin of error
        dxI = landmarks[0][lid["ITip"]][x] - landmarks[0][lid["IPip"]][x]
        dyI = landmarks[0][lid["ITip"]][y] - landmarks[0][lid["IPip"]][y]
        dxP = landmarks[0][lid["PTip"]][x] - landmarks[0][lid["PPip"]][x]
        dyP = landmarks[0][lid["PTip"]][y] - landmarks[0][lid["PPip"]][y]
        dxT = landmarks[0][lid["TTip"]][x] - landmarks[0][lid["TPip"]][x]
        dyT = landmarks[0][lid["TTip"]][y] - landmarks[0][lid["TPip"]][y]
        dxM = landmarks[0][lid["MTip"]][x] - landmarks[0][lid["MPip"]][x]
        dyM = landmarks[0][lid["MTip"]][y] - landmarks[0][lid["MPip"]][y]
        dxR = landmarks[0][lid["RTip"]][x] - landmarks[0][lid["RPip"]][x]
        dyR = landmarks[0][lid["RTip"]][y] - landmarks[0][lid["RPip"]][y]
        
        states = [
            dyI < 0 and abs(dyI) >= abs(dxI), # index up         [0]
            dyP < 0 and abs(dyP) >= abs(dxP), # pinky up         [1]
            dyR < 0 and abs(dyR) >= abs(dxR), # ring up          [2]
            dyM < 0 and abs(dyM) >= abs(dxM), # middle up        [3]
            dyT < 0 and abs(dyT)*0.5 >= abs(dxT), # thumb up     [4]
            dxI > 0 and abs(dyI)/moe < abs(dxI), # index  right  [5]
            dxI < 0 and abs(dyI)/moe < abs(dxI), # index left    [6]
            dxP > 0 and abs(dyP)/moe < abs(dxP), # pinky right   [7]
            dxP < 0 and abs(dyP)/moe < abs(dxP), # pinky left    [8]
            dxR > 0 and abs(dyR)/moe < abs(dxR), # ring right    [9]
            dxR < 0 and abs(dyR)/moe < abs(dxR), # ring left     [10]
            dxM > 0 and abs(dyM)/moe < abs(dxM), # middle  right [11]
            dxM < 0 and abs(dyM)/moe < abs(dxM), # middle left   [12]
            dxT > 0 and abs(dyT)/moe < abs(dxT), # thumb right   [13]
            dxT < 0 and abs(dyT)/moe < abs(dxT)  # thumb left    [14]
            

        ]

        fingers_up = states[:5].count(True)
        fingers_left = states[5:13:2].count(True)
        fingers_right = states[6:13:2].count(True)

        if (fingers_left >= 4 or fingers_right >= 4) and landmarks[0][lid["TPip"]][y] < landmarks[0][lid["IPip"]][y]:
            if fingers_left >= 4 and landmarks[0][lid["TPip"]][x] > landmarks[0][lid["IPip"]][x]:
                print("Thumbs up")
            elif fingers_right >= 4 and landmarks[0][lid["TPip"]][x] < landmarks[0][lid["IPip"]][x]:
                print("Thumbs up")
            else:
                print("Boi")
        elif states[0] and states[3] and fingers_up == 2:
            print("Peace")
        elif states[3] and ((fingers_up == 1) or (states[13] or states[14]) or (states[4] and fingers_up == 2)):
            print("Fuck you")
        elif (states[5] and fingers_left == 1) or (states[6] and fingers_right == 1):
            if states[4]:
                print("Pewpew")
            else:
                print("pointing")
        elif states[4] and states[:4].count(True) <= 0 and fingers_left + fingers_right == 0:
            print("A")
        
        elif states[4] and fingers_up == 0:
            print("Thumbs up man")

        else:
            if fingers_up > 0:
                print(fingers_up)
            else:
                print("Nothing")
   

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 27:
        break
