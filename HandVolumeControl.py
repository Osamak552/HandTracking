import cv2
import time
import math
import mediapipe
import numpy as np
import HandTrackingMod as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap = cv2.VideoCapture(0)

pTime = 0

cTime = 0

detector = htm.HandTracker(minDetectionConfidence=0.6)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume.GetVolumeRange()

while True:
    sucess, img = cap.read()
    detector.DetectingHands(img)
    landMarks = detector.getHandCoordinates(img)

    if len(landMarks) != 0:

        x1, y1 = landMarks[4][1], landMarks[4][2]
        x2, y2 = landMarks[8][1], landMarks[8][2]

        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 12, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (255, 0, 0), cv2.FILLED)

        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)


        cv2.line(img,(x1,y1),(x2,y2),(200,0,0),3)

        length = math.hypot(x2-x1, y2-y1)

        if length < 50:
            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)
        if length >=190:
            cv2.circle(img, (cx, cy), 8, (51, 51, 255), cv2.FILLED)

        if length > 150:
            col = np.interp(length,[150,200],[102,0])
            cv2.line(img, (x1, y1), (x2, y2), (col, col, 255), 3)



        vol = np.interp(length,[50,200],[-65,0])
        print(vol)


        volume.SetMasterVolumeLevel(vol, None)






    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (200, 0, 200), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
