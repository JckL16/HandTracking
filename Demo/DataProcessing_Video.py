import Module
import cv2
import os
import random
import time
import imageio

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

tpi = 0.5 # time per image
number_of_images = 100

landmarks = []

img_list = []

# Låter detector hitta händer innan den börjar analysera bilderna som ska användas
while len(landmarks) == 0:
    img = cv2.imread(os.path.join(picture_path, files[random.randrange(total_files-1)]))
    img = detector.findHands(img, draw=False)
    landmarks = detector.getPositions()


for number, file in enumerate(files[:number_of_images]):
    done = False
    img = cv2.imread(os.path.join(picture_path, file))

    img = detector.findHands(cv2.resize(img, (w*3, h*3)))
    landmarks = detector.getPositions()

    cv2.putText(img=img, text=file[-6], org=(15, 40), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 255, 255),thickness=2)

    if len(landmarks) != 0:
        if len(landmarks[0]) == 21:
            x_max, x_min, y_max, y_min = 0, w, 0, h
            for landmark in landmarks[0]:
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
            while True:
                if cv2.waitKey(0) == ord("q"):
                    img_list.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    break
                elif cv2.waitKey(0) == ord("e"):
                    break
                elif cv2.waitKey(0) == 27:
                    done = True
                    break

            print(number)
    if done:
        break

imageio.mimsave(r"demo.gif", img_list, fps=1/tpi)
