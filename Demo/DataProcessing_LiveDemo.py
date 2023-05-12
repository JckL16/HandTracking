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


write_path = "Data.csv"
if os.path.exists(write_path):
    os.remove(write_path)
data_file = open(write_path, "a", newline="")
writer_object = writer(data_file)


h, w, _ = cv2.imread(os.path.join(picture_path, files[0])).shape

bounding_offset = 10


for number, file in enumerate(files):
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

                width, height = x_max - x_min, y_max - y_min

                # print(round((int(current_hand[0][1] * w) - x_min) / width, decimal_precision), round((int(current_hand[0][2]*h) - y_min) / height, decimal_precision))
                # print()

                new_poses = [file[-6], hands[file[-5]]]

                for index in used_landmarks:
                    # new_poses.append([index, round((int(current_hand[index][1] * w) - x_min) / width, decimal_precision), round((int(current_hand[index][2]*h) - y_min) / height, decimal_precision)])
                    new_poses.append(round((int(current_hand[index][1] * w) - x_min) / width, decimal_precision))
                    new_poses.append(round((int(current_hand[index][2] * h) - y_min) / height, decimal_precision))


                print(new_poses)
                writer_object.writerow(new_poses)

                print(f"{number} / {total_files} - {round(number/total_files * 100, 2)}%")

                cv2.rectangle(img, (x_min*3 - bounding_offset, y_min*3 - bounding_offset),
                                   (x_max*3 + bounding_offset, y_max*3 + bounding_offset), (0,100,0), 2)

                cv2.imshow("Image", img)

                cv2.waitKey(27)

                time.sleep(0.5)
