import Module as m
import cv2

cap = cv2.VideoCapture(0)
detector = m.handDetector()

while True:
    success, img = cap.read()

    img = detector.findHands(img)

    landmarks = detector.getPositions(img)
    if len(landmarks) != 0: # Dubbelkollar att den faktiskt hittar en eller flera händer
        print(landmark)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 27:
        break
