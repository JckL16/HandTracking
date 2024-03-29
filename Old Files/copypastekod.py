import cv2
import mediapipe as mp

mphands = mp.solutions.hands
hands = mphands.Hands()
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

_, frame = cap.read()

h, w, c = frame.shape

while True:
    _, frame = cap.read()
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)
    hand_landmarks = result.multi_hand_landmarks
    if hand_landmarks:
        for handLMs in hand_landmarks:
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h
            for lm in handLMs.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y

        for i in hand_landmarks:
            print(len(i.landmark))

        cv2.rectangle(frame, (x_min, y_min),
                      (x_max, y_max), (0, 255, 0), 2)
        margin = 10

        hand_frame = frame[y_min-margin:y_max
                           + margin, x_min-margin:x_max+margin]

        if hand_frame is not None:

            hand_frame = cv2.resize(hand_frame, (300, 300))

            cv2.imshow("picture", hand_frame)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break
