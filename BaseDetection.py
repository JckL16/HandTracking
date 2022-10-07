import Module as m
import cv2
import math

cap = cv2.VideoCapture(0)
detector = m.handDetector()

print("Started")

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
            dyI < 0 and abs(dyI) >= abs(dxI), # index up
            dyP < 0 and abs(dyP) >= abs(dxP), # pinky up 
            dyR < 0 and abs(dyR) >= abs(dxR), # ring up 
            dyM < 0 and abs(dyM) >= abs(dxM), # middle up
            dyT < 0 and abs(dyT)*0.5 >= abs(dxT), # thumb up
            dxI > 0 and abs(dyI)/moe < abs(dxI), # index  right
            dxI < 0 and abs(dyI)/moe < abs(dxI), # index left
            dxP > 0 and abs(dyP)/moe < abs(dxP), # pinky right
            dxP < 0 and abs(dyP)/moe < abs(dxP), # pinky left
            dxR > 0 and abs(dyR)/moe < abs(dxR), # ring right
            dxR < 0 and abs(dyR)/moe < abs(dxR), # ring left
            dxM > 0 and abs(dyM)/moe < abs(dxM), # middle  right
            dxM < 0 and abs(dyM)/moe < abs(dxM), # middle left
            dxT > 0 and abs(dyT)/moe < abs(dxT), # thumb right
            dxT < 0 and abs(dyT)/moe < abs(dxT)  # thumb left
            

        ]

        # print(states[:5].count(True))    # Number of fingers up
        #print(states[5::2].count(True))  # Number of fingers to the left
        #print(states[6::2].count(True))  # Number of fingers to the right
        # print(states[4], states[13], states[14])

        if (states[5::2].count(True) >= 4 or states[6::2].count(True) >= 4) and landmarks[0][lid["TPip"]][y] < landmarks[0][lid["IPip"]][y]:
            print("Boi")
        elif states[0] and states[3] and states[:5].count(True) == 2:
            print("Peace")
        elif states[3] and ((states[:5].count(True) == 1) or (states[13] or states[14]) or (states[4] and states[:5].count(True) == 2)):
            print("Fuck you")
        elif states[4] and ((states[5] and states[5::2].count(True) == 1) or (states[6] and states[6::2].count(True) == 1)):
            print("Pewpew")
        else:
            print("Nothing")
        #1
        '''count = 0
        for j in range(2,19,4):
            if landmarks[0][j][y] >= landmarks[0][j+2][y]:
                count += 1
        print(count)'''




    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 27:
        break
