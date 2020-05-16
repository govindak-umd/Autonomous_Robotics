from picamera import PiCamera
from time import sleep
import cv2
camera = PiCamera()
camera.start_preview()
sleep(10)
camera.capture('orange_final.jpg')
img = cv2.imread('orange_final.jpg',1)
img = cv2.flip(img,-1)
cv2.imwrite('orange_final.jpg',img)
camera.stop_preview()
