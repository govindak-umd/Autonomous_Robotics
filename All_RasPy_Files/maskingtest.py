import cv2
import imutils
import numpy as np
img = cv2.imread('testudo.jpg')
img_red = img[:,:,2]
cv2.imshow('image',img_red)



cv2.waitKey(0)
