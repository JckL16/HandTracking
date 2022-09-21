import Module as m # importar modulen som skapats
import cv2
import os


path = r"F:\SignLanguageDataset\asl_dataset" # Directory till mappen med fler mappar för varje bokstav/tecken/siffra

dirlist = [x[0] for x in os.walk(path)][1:] # Skaffar en lista på alla mappar i directoryn, första är startdirectory så den behöver den inte kolla på

detector = m.handDetector()

for dir in dirlist: # För varje map i directoryn

    f = open(r"ProcessedData//" + dir.split("\\")[-1] + ".txt", "a") # Skapar och skriver till en fil med samma namn som mappen som öppnas i mappen "ProcessedData"

    for root, dirs, files in os.walk(dir): # Hittar alla filer i mappen
        for file in files: # Loopar genom alla filer
            img = cv2.imread(dir + "//" + file)  # Läser varje bild till en numpy array som detectorn kan använda
            img = detector.findHands(img, draw=False) # Hittar händerna
            landmarks = detector.getPositions(img) # Ger landmarksen på händerna
            landmarkStr = "" # En string som senare kan appendas till textfilen
            if landmarks: # Kollar att den faktiskt hittade några landmarks
                for index in range(20): # Loopar genom alla landmark index och lägger till dem i stringen, med ett " - " mellan för separation
                    landmarkStr += str(landmarks[0][index])[1:-1] + " - "
            f.write(landmarkStr[:-3] + "\n") # Lägger till alla landmark positioner i textfilen, [:-3] är för att slippa " - " på slutet och \n för att separera alla olika bilders landmarks

    f.close() # Du borde veta vad detta gör

    print(f"{dir} is done!") # Status update, programmet tar piss lång tid med många olika mappar
