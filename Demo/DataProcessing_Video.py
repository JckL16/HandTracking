import Module
import cv2
import os
from csv import writer
import random
import time

# Data Format :
# | Tecken |     Hand     | Landmark 1x | Landmark 1y | Landmark 2x osv
# ------------------------------------------------------------------
# |  0-5   | L = 0, R = 1 |             |             |

hands = {
    "L" : 0,
    "R" : 1
}

detector = Module.handDetector()

used_landmarks = [0, 2, 4, 5, 8, 9, 12, 13, 16, 17, 20]

decimal_precision = 10

picture_path = r"D:\SignLanguageDataset\Numbers\Mixed"

files = os.listdir(picture_path)
random.shuffle(files)
total_files = len(files)


h, w, _ = cv2.imread(os.path.join(picture_path, files[0])).shape

bounding_offset = 10

frame_rate = 24
tpi = 2.5 # time per image

img_list = []

number_of_images = 30

for number, file in enumerate(files[:number_of_images]):
    img = cv2.imread(os.path.join(picture_path, file))
    img = cv2.resize(img, (w*3, h*3))


    img = detector.findHands(img)
    landmarks = detector.getPositions()

    cv2.putText(img=img, text=file[-6], org=(15, 40), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 255, 255),thickness=2)

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

                cv2.rectangle(img, (x_min*3 - bounding_offset, y_min*3 - bounding_offset),
                                   (x_max*3 + bounding_offset, y_max*3 + bounding_offset), (0,100,0), 2)

                cv2.imshow("Image", img)
                cv2.waitKey(27)
                time.sleep(0.1)
                print(number)
                # for i in range(int(frame_rate * tpi)):
                img_list.append(img)


video = cv2.VideoWriter("Demo.mp4", cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (w,h))

for img in img_list:
    video.write(img)

video.release()
