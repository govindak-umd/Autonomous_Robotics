import cv2
import imutils
import numpy as np
canvas = np.zeros((500,500,3),dtype='uint8')
green = (8,255,0)

cv2.line(canvas,(0,0),(200,300),green)


cv2.imshow("canvas",canvas)
cv2.waitKey(0)
