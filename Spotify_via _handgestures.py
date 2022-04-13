import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import mediapipe as mp
import pyautogui as g
import time


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
bgimages =[]
for i in os.listdir("/Users/shashwateshtripathi/Downloads/images2"):
    bgimages.append(cv2.imread(f"/Users/shashwateshtripathi/Downloads/images2/{i}"))

segmentor = SelfiSegmentation(1)
index =0
inside = False
right = False
left = False
i=0
while(True):
    success,image = cap.read() 
    if(i>3):
       # img2 = segmentor.removeBG(img,(255,255,255),threshold = 0.6) 
        bgimage = cv2.resize(bgimages[index],(1280,720))
        img = segmentor.removeBG(image,bgimage,threshold = 0.4)
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        multiLandMarks = results.multi_hand_landmarks
        if multiLandMarks:
            handPoints=[]
            for handLms in multiLandMarks:
                mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
                for idx , lm in enumerate(handLms.landmark):
                    h,w,c = img.shape
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    handPoints.append((cx,cy))
            if not left and handPoints[8][0]<340:
                left = True
                index=index-1
                index=index%len(bgimages)
                g.keyDown('command')
                g.press('space')
                g.keyUp("command")
                g.write('Spotify')
                g.hotkey('enter')
                g.keyDown("command")
                g.press('left')
                g.press( 'h')
                g.keyUp("command")
                g.click()
            if not right and handPoints[8][0]>940:
                right = True
                index = index+1
                index=index%len(bgimages)
                g.keyDown('command')
                g.press('space')
                g.keyUp("command")
                time.sleep(0.5)
                g.typewrite('Spotify')
                g.hotkey('enter')
                time.sleep(1)
                g.keyDown("command")
                g.press('right')
                g.press('h')
                g.keyUp("command")
                g.click()
            if handPoints[8][0] > 340 and handPoints[8][0]<940:
                right = False
                left = False
            
        imgstack = cvzone.stackImages([image,img],2,1)
        cv2.imshow("Video",imgstack)
    key = cv2.waitKey(1)
    i=i+1