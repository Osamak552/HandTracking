import cv2
import mediapipe as mp
import time


class HandTracker():
    def __init__(self,mode = False,maxNoHands = 2,minDetectionConfidence=0.5,minTrackingConfidence=0.5):
        self.Mode = mode
        self.MaxNoHands = maxNoHands
        self.MinDetectionConfidence = minDetectionConfidence
        self.MinTrackingConfidence = minTrackingConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.Mode,self.MaxNoHands,
                                        self.MinDetectionConfidence,self.MinTrackingConfidence)
        self.mpDraw = mp.solutions.drawing_utils

    def DetectingHands(self,img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.result = self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:


                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def getHandCoordinates(self, img,handno = 0):


        lst = []
        if  self.result.multi_hand_landmarks:
            handLms = self.result.multi_hand_landmarks[handno]
            for id, lm in enumerate(handLms.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lst.append([id,cx,cy])

                # if id == 4:
                #     cv2.circle(img, (cx,cy), 10, (255,0,255),cv2.FILLED)
        return lst





def main():

    pTime = 0

    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = HandTracker()
    while True:
        success, img = cap.read()

        img = detector.DetectingHands(img)

        lst = detector.getHandCoordinates(img)
        if len(lst) != 0:
            print(lst)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (200, 0, 200), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()