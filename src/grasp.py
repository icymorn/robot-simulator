import cv2
import time
import numpy as np
import servo
from robotArm import robotArm

# if __name__ == '__main__':
#
#     arm = robotArm()
#     servoServer = servo.ServoServer(arm)
#     rotatelist = [-90, -45, 0, 45, 90]
#     servoServer.moveTo(0.13, 0.12)
#     i = random.randint(0, 4)
#     servoServer.rotate(rotatelist[i])
#     servoServer.open()
#     servoServer.moveTo(0.16, 0.08)
#     servoServer.close()
#     servoServer.moveTo(0.13, 0.12)
#     servoServer.open()
#     time.sleep(3)
#     print "================ reset"
#     servoServer.reset()
#     time.sleep(10)

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,1))
fgbg = cv2.BackgroundSubtractorMOG()

n = 0
while n < 10:
    _, frame = cap.read()
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    n += 1

print "applied"
time.sleep(5)

m = 0


while m < 1000:
    _, frame = cap.read()
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    maxcontour = None
    maxarea    = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > maxarea:
            maxarea = area
            maxcontour = contour

    if maxcontour is not None:
        x,y,w,h = cv2.boundingRect(maxcontour)

        rect = cv2.minAreaRect(maxcontour)
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        if rect[1][0] < rect[1][1]:
            cv2.putText(frame, "w%.0f h%.0f r%.0f" % (rect[1][1], rect[1][0], - 90 - rect[2]), (int(rect[0][0]), int(rect[0][1])), font, 1.05,(0,0,255),2)     
        else:
            cv2.putText(frame, "w%.0f h%.0f r%.0f" % (rect[1][0], rect[1][1], -rect[2]), (int(rect[0][0]), int(rect[0][1])), font, 1.05,(0,0,255),2)            

    cv2.imshow('frame',frame)
    m += 1

cv2.waitKey(0)