#Python v3, OpenCV v3.4.2

import numpy as np
import cv2

videoCapture = cv2.VideoCapture("video.mp4")
ret,camera_input = videoCapture.read()
rows, cols = camera_input.shape[:2]

w = 10 
h = 15
col = int((cols - w) / 2)
row = int((rows - h) / 2)
shiftWindow = (col, row, w, h)

roi = camera_input[row:row + h, col:col + w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
histogram = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(histogram,histogram,0,255,cv2.NORM_MINMAX)


term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while True:

    #Video'dan bir frame okur
    ret ,camera_input = videoCapture.read()

    hsv = cv2.cvtColor(camera_input, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],histogram,[0,180],1)
    
    #her yeni konum için meanshift tekrar uygular
    ret, shiftWindow = cv2.CamShift(dst, shiftWindow, term_crit)
  
     #Görüntü üzerinde tespit edilen alanı çizer
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)
    result_image = cv2.polylines(camera_input,[pts],True, 255,2)
   
   
    cv2.imshow('Camshift (Surekli Mean Shift) Algoritmasi', result_image)
    k = cv2.waitKey(60) & 0xff

videoCapture.release()
cv2.destroyAllWindows()