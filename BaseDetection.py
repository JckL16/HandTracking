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

}

x, y = 1,2


while True:
    success, img = cap.read()

    img = detector.findHands(img)

    landmarks = detector.getPositions()
    if len(landmarks) != 0: # Dubbelkollar att den faktiskt hittar en eller flera händer

        #print(landmarks[0][::4])
        if all(i[y] >= landmarks[0][lid["TTip"]][y] for i in (landmarks[0][::4])):
            print("Thumbs up")
        else:
            print("NO")



    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 27:
        break
