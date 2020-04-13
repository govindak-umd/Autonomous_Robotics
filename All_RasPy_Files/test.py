import cv2
import imutils
import numpy as np

print("all is good")
image  = cv2.imread("testudo.jpg")
image = imutils.resize(image,width=480)
cv2.imshow("testimage",image)
blurred = np.hstack([cv2.GaussianBlur(image,(3,3),0),cv2.GaussianBlur(image,(21,21),0)])
cv2.imshow("blurred",blurred)
#while True:
#	if cv2.waitKey(0) & 0xFF='127':
#		break
cv2.waitKey(0)
