import cv2
import numpy as np
import time
#initialize cam
cam= cv2.VideoCapture(0)
fps = cam.get(cv2.CAP_PROP_FPS)
timestamps = [cam.get(cv2.CAP_PROP_POS_MSEC)]
calc_timestamps = [0.0]
#codec for saving
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 10, (640,480))
while True:
    _, frame = cam.read()
    #record beginning of frame
    startTime = time.time()
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([55,100,100])
    upper_green =  np.array([86,255,255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    img,contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #draw circles
    for contour in contours:
        cv2.drawContours(frame, contour, -1, (0, 0, 255), 3)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    out.write(frame)
    #record end of frame and find frame delay delta
    time_frame = time.time() - startTime 
    f = open('Frame_data.txt','a')
    #time difference between frames
    f.write(str(time_frame))
    f.write('\n')
    print('Frame difference', time_frame)
    key = cv2.waitKey(100) & 0xFF
    if key == 27:
        break
f.close()       
cam.release()
out.release()
cv2.destroyAllWindows()