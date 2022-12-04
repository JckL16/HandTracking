from re import X
import Module
import cv2

detector = Module.handDetector()

cap = cv2.VideoCapture(0)

used_landmarks = [0, 2, 4, 5, 8, 9, 12, 13, 16, 17, 20]

decimal_precision = 7

while True:
    _, img=cap.read()

    h, w, _ = img.shape

    img = detector.findHands(img, draw=False)
    landmarks = detector.getPositions()

    if len(landmarks) != 0:
        for current_hand in landmarks:
            if len(current_hand) == 21:
                x_max, x_min, y_max, y_min = 0, w, 0, h
                for landmark in current_hand:
                    x, y = int(landmark[1] * w), int(landmark[2] * h)

                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y

                width, height = x_max - x_min, y_max - y_min

                # print(round((int(current_hand[0][1] * w) - x_min) / width, decimal_precision), round((int(current_hand[0][2]*h) - y_min) / height, decimal_precision))
                # print()

                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                new_poses = []

                for index in used_landmarks:
                    new_poses.append([index, round((int(current_hand[index][1] * w) - x_min) / width, decimal_precision), round((int(current_hand[index][2]*h) - y_min) / height, v)])

                for row in new_poses:
                    print(row)
                print()


    cv2.imshow("Fuck", img)
    if cv2.waitKey(1) == 27:
        break
