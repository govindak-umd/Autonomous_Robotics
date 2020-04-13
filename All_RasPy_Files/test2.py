import cv2
import imutils
import numpy as np

image = cv2.imread("testudo.jpg")
image = imutils.resize(image,width=400)
cv2.imshow("image",image)
cv2.waitKey(0)
