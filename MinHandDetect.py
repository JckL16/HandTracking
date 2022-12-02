from re import X
import Module
import cv2

detector = Module.handDetector()

cap = cv2.VideoCapture(0)

used_landmarks = [0, 2, 4, 5, 8,  9, 12, 13, 16, 17, 20]

while True:
    _,img=cap.read()

    h, w, _ = img.shape

    img = detector.findHands(img, draw=False)
    landmarks = detector.getPositions()

    if len(landmarks) != 0:
        for current_hand in landmarks:

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

                width = x_max - x_min
                height = y_max - y_min

                '''print(x_min, x_max)
                print(y_min, y_max)
                print(width, height)
                print(int(current_hand[0][1] * w) - x_min, int(current_hand[0][2]*h) - y_min)
                print()'''


                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)


                new_poses = []

                cv2.rectangle(img, (x_min, y_min), (int(current_hand[0][1] * w), int(current_hand[0][2]*h)), (0, 255, 0), 2)

                for index in used_landmarks:

                    #new_poses.append([index, ((int(current_hand[index][1]) * w) - x_min) / width, ((int(current_hand[index][2]) * h) - y_min) / height])
                    # print([index, ((int(current_hand[index][1]) * w) - x_min) / width, ((int(current_hand[index][2]) * h) - y_min) / height])
                    print((int(current_hand[index][1]) * w) - x_min, (int(current_hand[index][2]) * h) - y_min)



    cv2.imshow("Fuck", img)
    if cv2.waitKey(1) == 27:
        break
