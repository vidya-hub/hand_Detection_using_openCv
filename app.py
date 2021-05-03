from cv2 import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRgb)
    if results.multi_hand_landmarks:
        print(len(results.multi_hand_landmarks))
        hands_list=[]
        for handLndms in (results.multi_hand_landmarks):
            hand=[]
            for id, lm in enumerate(handLndms.landmark):
                h, w, c = img.shape
                hx, hy = int(lm.x*w), int(lm.y*h)
                hand.append([id, hx, hy])
                
                # print(id, hx, hy)
            hands_list.append(hand)
            mpDraw.draw_landmarks(img, handLndms, mpHands.HAND_CONNECTIONS)
        print(hands_list)
    cv2.imshow(" original ", img)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
