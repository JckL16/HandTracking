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

        moe = math.pi/4 #Margin of error
        dxI = landmarks[0][lid["ITip"]][x] - landmarks[0][lid["IPip"]][x]
        dyI = landmarks[0][lid["ITip"]][y] - landmarks[0][lid["IPip"]][y]
        dxP = landmarks[0][lid["PTip"]][x] - landmarks[0][lid["PPip"]][x]
        dyP = landmarks[0][lid["PTip"]][y] - landmarks[0][lid["PPip"]][y]
        dxM = landmarks[0][lid["MTip"]][x] - landmarks[0][lid["MPip"]][x]
        dyM = landmarks[0][lid["MTip"]][y] - landmarks[0][lid["MPip"]][y]
        dxR = landmarks[0][lid["RTip"]][x] - landmarks[0][lid["RPip"]][x]
        dyR = landmarks[0][lid["RTip"]][y] - landmarks[0][lid["RPip"]][y]
        states = [
            dyI < 0 and abs(dyI) >= abs(dxI), # index_up
            dyP < 0 and abs(dyP) >= abs(dxP), # pinky_up 
            dyR < 0 and abs(dyR) >= abs(dxR), # ring_up 
            dyM < 0 and abs(dyM) >= abs(dxM) # middle_up
        ]

        print(states[:4].count(True))

        #1
        '''count = 0
        for j in range(2,19,4):
            if landmarks[0][j][y] >= landmarks[0][j+2][y]:
                count += 1
        print(count)'''




    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 27:
        break
