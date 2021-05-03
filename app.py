from cv2 import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=1,
)
def findDistance(points,cors):
    first=cors[points[1]]
    sec=cors[0]
    distance = int(
            (((sec[1]-first[1])**2)+((sec[0]-first[0])**2))**(0.5))
    return distance
mpDraw = mp.solutions.drawing_utils
fingertips = {"thumb": [2, 4], "index": [6, 8], "middle": [
    10, 11], "ring": [14, 16], "pinky": [18, 20], }
while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRgb)
    if results.multi_hand_landmarks:
        hands_list = []
        for handLndms in (results.multi_hand_landmarks):
            hand = {}
            for id, lm in enumerate(handLndms.landmark):
                h, w, c = img.shape
                hx, hy = int(lm.x*w), int(lm.y*h)
                hand[id] = (hx, hy)
                cv2.putText(img, str(id), (hx, hy),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 255, 0), 1)
            hands_list.append(hand)
            mpDraw.draw_landmarks(img, handLndms, mpHands.HAND_CONNECTIONS)
        filteredfingers=[(findDistance(fingertips[fingerkeys],hand))<150 for fingerkeys in fingertips.keys()]
        closedfingers=[filteredfinger for filteredfinger in filteredfingers if not filteredfinger ]
        cv2.putText(img, str(len(closedfingers)), (50, 50),
                    cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 0, 255), 2)
        # for keys in fingertips.keys():
        #     distnce=findDistance(fingertips[keys],hand)
        #     print(f"distance of {keys} is closed {distnce<150}")
        # cv2.circle(img, hand[4], 5, (255, 0, 0), -1)
        # cv2.circle(img, hand[8], 5, (255, 0, 0), -1)
        # thumb = hand[4]
        # second_finger = hand[8]
        # distance = int(
        #     (((second_finger[1]-thumb[1])**2)+((second_finger[0]-thumb[0])**2))**(0.5))
        # print(distance)
        # cv2.putText(img, str(distance), (50, 50),
        #             cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 0, 255), 2)
        # print((hands_list))
    cv2.imshow(" original ", img)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
