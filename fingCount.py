import cv2
import time
import os
import handTrackingModule as htm

wCam, hCam = 2800, 1250

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

FolderPath = 'img'
myList = os.listdir(FolderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{FolderPath}/{imPath}')
    overlayList.append(image)#udin hadala dena path eka save karaganne meya

tipids = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()


    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) !=0:
        fingers = []
        #tham
        if lmList[tipids[0]][1] > lmList[tipids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #4 fingers
        for id in range(1,5):
            if lmList[tipids[id]][2]< lmList[tipids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        totalFingers = fingers.count(1)#1 thiyanana sankayawa kiyada fingers kiyana list eke
        print(totalFingers)
        h, w, c = overlayList[totalFingers-1].shape
        # print(f'{h,w,c}')
        img[0:h, 0:w] = overlayList[totalFingers-1]

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'fst : {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3 )
    cv2.imshow("img", img)
    cv2.waitKey(1)
