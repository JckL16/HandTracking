import cv2
import mediapipe as mp
import time

# Skapa ett objekt som kan hämta video från kamera
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands # Starta en iteration av en class som trackar händer

hands = mpHands.Hands( # Alla inställningar nedan är standard men ville att vi förstår dem
    static_image_mode=False, # False låter programmet tracka punkter på handen och inte bara detecta om den känner sig säker, gör programmet mycket snabbare
    max_num_hands=2, # Maximala mängden händer den trackar samtidigt
    min_detection_confidence=0.5, # Om programmet känner sig under 50% (i detta fall) säker på vart handen eller fingrarna ör, gör ny detection
    min_tracking_confidence=0.5
)

mpDraw = mp.solutions.drawing_utils # Module som används för att rita upp händerna

previous_time = time.time() # används senare för att beräkna fps

while True: # Runnar tills man stänger ner programmet
    success, img = cap.read() # Succes är om den lyckades captura från kameran, img är en numpy array av alla pixlar i format BGR

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # img skrivs från början i format BGR, men mediapipe kräver RGB, detta omvandlar

    results = hands.process(imgRGB) # Berättar vart alla punker och liknande är i bilden

    if results.multi_hand_landmarks: # Kollar om den faktiskt hittar några händer. Om inte ger den None
        for hand in results.multi_hand_landmarks: # Om det är fler händer som detectas så måste båda dessa ritas upp
            for id, landmark in enumerate(hand.landmark): # Id = vilket id en viss punkt på handen har, landmark är vart den är i bilden i form av en ratio, x = 0.5 => xkord = screenwidth*0.5
                screenHeight, screenWidth, _ = img.shape # Ger storleken på den bild som kameran tar
                pointx = int(landmark.x*screenWidth) # Ger pixel positionen för den nuvarande landmarken som beräknas
                pointy = int(landmark.y*screenHeight)
                print(pointx,pointy)
            mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS) # Ritar landmarks för vissa punkter på varje hand, samt streck mellan dem

    print(results)

    # För att beräkna fps
    fps = 1/(time.time()-previous_time)
    previous_time = time.time()

    cv2.putText(img, str(round(fps, 0)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 3)

    cv2.imshow("Image", img) # Visar bilden som capturas ovan i ett fönster med titel Image

    if cv2.waitKey(1) == 27: # Om man trycker på esc stäng programmet
        break
