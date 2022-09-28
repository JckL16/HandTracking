import Module as m
import cv2

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
        
        #print(landmarks[0][2::4][y], landmarks[0][lid["TTip"]][y])

        #print(landmarks[0][2::4])
        #print(landmarks[0][0::4][1:])
        
        '''for j in (landmarks[0][::4][1:]):
            print(type(landmarks[0][2::4][y]))'''

        '''print(range(2,18,4))
        for i in range(2,19,4):
            print(i)'''
        #1
        print(type(landmarks[0][j][y] <= landmarks[0][j+2][y] for j in range(2,19,4)))
        '''count = 0
        if (landmarks[0][j][y] <= landmarks[0][j+2][y] for j in range(2,19,4)):
            count += 1
        print(count)'''



        

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 27:
        break
