from re import X
import Module
import cv2

detector = Module.handDetector()

cap = cv2.VideoCapture(0)

while True:
    _,img=cap.read()

    h, w, _ = img.shape

    img = detector.findHands(img, draw=False)
    landmarks = detector.getPositions()

    if len(landmarks) != 0:    
        for index, current_hand in enumerate(landmarks):
            if len(current_hand) == 21:
                x_max, x_min, y_max, y_min = 0, w, 0, h
                for landmark in current_hand:
                    x = int(landmark[1] * w)
                    y = int(landmark[2] * h)

                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y

                margin = 10

                if margin+ x_max > w or margin + y_max > h:
                    continue

                try:  
                    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    hand_frame = img[y_min-margin:y_max+margin, x_min-margin:x_max+margin]

                    if hand_frame is not None:
                        hand_frame = cv2.resize(hand_frame, (300, 300))

                    #cv2.imshow(f"hand {index}", hand_frame)
                    

                    hand_frame = detector.findHands(hand_frame)

                    cv2.imshow("Hand", hand_frame)
                except:
                    continue

            


    cv2.imshow("Fuck", img)
    if cv2.waitKey(1) == 27:
        break

    