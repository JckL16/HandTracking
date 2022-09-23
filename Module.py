import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, max_hands=2, detection_confidence = 0.5, tracking_confidence=0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True): # Hittar och, om man vill, ritar vart alla landmarks är
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)

        return img

    def getPositions(self): # Om man vill ha exakt vart på skärmen olika landmarks är kan man använda denna funktion
        landmark_list = []

        # Hela detta block skapar en lista med positioner för alla landmarks på x antal händer
        # Så landmark nummer y (se bild) på hand x hamnar i listans index [x][y]
        if self.results.multi_hand_landmarks:
            for index, hand in enumerate(self.results.multi_hand_landmarks):
                landmark_list.append([])
                for nr, landmark in enumerate(hand.landmark):
                    landmark_list[index].append([nr, landmark.x, landmark.y])

        return landmark_list

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)

        landmarks = detector.getPositions()
        if len(landmarks) != 0: # Dubbelkollar att den faktiskt hittar en eller flera händer
            pass # Gör vad som vill göras med infon

        cv2.imshow("Image", img)

        cv2.waitKey(1)

if __name__ == "__main__":
    main()
