import Module as m
import cv2
import math

cap = cv2.VideoCapture(1)
detector = m.handDetector()

lid={ #Landmark ID
    "W": 0,
    #Fingertips
    "TTip": 4,   # Thumb tip
    "ITip": 8,   # Index tip
    "MTip": 12,  # Middle tip
    "RTip": 16,  # Ring tip
    "PTip": 20,  # Pinky tip
    #pips (Knogen vid varje finger)
    "TPip": 2,
    "IPip": 6,
    "MPip": 10,
    "RPip": 14,
    "PPip": 18,


}

X, Y = 1,2 # Fasta värden


while True:
    success, img = cap.read()  # Fånga bilden från kameran samt se om den faktiskt får en bild

    img = detector.findHands(img)   # Hitta händerna

    landmarks = detector.getPositions()   # Få landmark positionerna på bilden i form av koordinater
    if len(landmarks) != 0: # Dubbelkollar att den faktiskt hittar en eller flera händer

        # Om det är höger eller vänster
        # -1 = vänster      1 = Höger
        currenthand = None
        if landmarks[0][lid["TPip"]][X] - landmarks[0][lid["PPip"]][X] > 0:
            currenthand = 1
        else:
            currenthand = -1


        #Tummen upp

        # abs(landmarks[0][lid["ITip"]][Y] - landmarks[0][lid["IPip"]][Y]) > moe

        moe = 0.75 #Margin of error (Hur rakt fingret måste vara pekat uppåt)

        # Dessa är värden på skillnadet i x värde mellan fingertopp och knoge för varje finger
        # I x respektiva y värde
        dxI = landmarks[0][lid["ITip"]][X] - landmarks[0][lid["IPip"]][X]
        dyI = landmarks[0][lid["ITip"]][Y] - landmarks[0][lid["IPip"]][Y]
        dxP = landmarks[0][lid["PTip"]][X] - landmarks[0][lid["PPip"]][X]
        dyP = landmarks[0][lid["PTip"]][Y] - landmarks[0][lid["PPip"]][Y]
        dxT = landmarks[0][lid["TTip"]][X] - landmarks[0][lid["TPip"]][X]
        dyT = landmarks[0][lid["TTip"]][Y] - landmarks[0][lid["TPip"]][Y]
        dxM = landmarks[0][lid["MTip"]][X] - landmarks[0][lid["MPip"]][X]
        dyM = landmarks[0][lid["MTip"]][Y] - landmarks[0][lid["MPip"]][Y]
        dxR = landmarks[0][lid["RTip"]][X] - landmarks[0][lid["RPip"]][X]
        dyR = landmarks[0][lid["RTip"]][Y] - landmarks[0][lid["RPip"]][Y]

        # Ett antal olika "states" som är användbara för att göra koden senare lättare att läsa
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
            dxM > 0 and abs(dyM)/moe < abs(dxM), # middle right [11]
            dxM < 0 and abs(dyM)/moe < abs(dxM),  # middle left   [12]
            dyT > 0 and abs(dyT)*0.5 <= abs(dxT), # thumb down     [13]


        ]

        result = None

        fingers_right = states[5:12:2].count(True)
        fingers_left =  states[6:12:2].count(True)

        fingers_up = states[:4].count(True)
        thumb_in = (landmarks[0][lid["TTip"]][X] - landmarks[0][lid["TPip"]][X])*currenthand < 0


        if thumb_in and fingers_up == 0:
            result = "0"
        if fingers_up == 0:
            if states[4]:
                if (currenthand == 1 and fingers_left == 0 and fingers_right != 0) or (currenthand == -1 and fingers_right == 0 and fingers_left != 0):
                    result = "Thumbs up"
            elif states[13]:
                if (currenthand == 1 and fingers_left == 0 and fingers_right != 0) or (currenthand == -1 and fingers_right == 0 and fingers_left != 0):
                    result = "Thumbs down"
        elif states[3] and fingers_up == 1:
            result = "Inte passande"
        elif not thumb_in:
            result = str(fingers_up + 1)
        elif fingers_up == 2 and thumb_in and states[0] and states[1]:
            result = "RockNRoll"
        else:
            result = str(fingers_up)


        cv2.putText(img=img, text=result, org=(20, 70), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0, 0, 0),thickness=2)


    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 27:
        break
