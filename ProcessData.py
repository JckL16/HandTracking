import Module as m # importar modulen som skapats
import cv2
import os


path = r"D:/SignLanguageDataset/Numbers/R" # Directory till mappen med fler mappar för varje bokstav/tecken/siffra
newPath = r"D:\SignLanguageDataset\NumbersProcessed"

dir_list = [x[0] for x in os.walk(path)][1:] # Skaffar en lista på alla mappar i directoryn, första är startdirectory så den behöver den inte kolla på

detector = m.handDetector()

for dir in dir_list:
    files = os.listdir(dir)
    print()
    for number,file in enumerate(files):
        if number == 0:
            txt_file = open(os.path.join(newPath, file[-6] + ".txt"), "a")
        if number % 50 == 0:
            print(number, "done")
        string = ""
        img = cv2.imread(os.path.join(dir,file))
        detector.findHands(img, draw=False)
        landmarks = detector.getPositions()
        if len(landmarks) > 0:
            for index in range(21):
                string += str(landmarks[0][index][1:])[1:-1] + " - "
            txt_file.write(string[:-3] + "\n")
        else:
            continue
