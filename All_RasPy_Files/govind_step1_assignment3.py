import numpy as np
import cv2 # OpenCV-Python
import matplotlib.pyplot as plt
import imutils
import time

img = cv2.imread("govind.jpg") 

if img is None:
    print ('Open Error')
else:
    print ('Image Loaded')
img = imutils.resize(img, width=500) #justto beable to see clearly
cv2.imshow('NORMAL IMAGE',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow('HSV IMAGE',hsv_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


#blank_canvas = np.zeros((1347, 1230,3),np.uint8)
lower_range = np.array([36, 25, 25])
upper_range = np.array([70, 255, 255])

blank_canvas = cv2.inRange(hsv_img, lower_range, upper_range)

cv2.imshow('Blank canvas', blank_canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()

edged = cv2.Canny(blank_canvas, 30, 200)  
img,contours,hierachy = cv2.findContours(blank_canvas,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cv2.imshow('Canny Edges After Contouring', edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Number of Contours found = " + str(len(contours))) 

cv2.drawContours(blank_canvas, contours, -1, (0, 255, 0), 3) 

cv2.imshow('Contours', blank_canvas) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 

#combined = np.hstack((img[:,:,1],hsv_img[:,:,1],blank_canvas))
#cv2.imshow('combined', combined) 
#cv2.waitKey(0) 
#cv2.destroyAllWindows()
print(' printing contours .. ')
print(contours)
all_contour_points = contours[0]

(x,y),radius = cv2.minEnclosingCircle(all_contour_points)
center = (int(x),int(y))
r = int(radius)
cv2.circle(img,center,r,(0,255,0),3)
cv2.circle(img,center,3,(255,255,0),3)
cv2.drawContours(img, [all_contour_points], 0, (0,0,255), 3)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cam= cv2.VideoCapture(0)
fps = cam.get(cv2.CAP_PROP_FPS)
timestamps = [cam.get(cv2.CAP_PROP_POS_MSEC)]
calc_timestamps = [0.0]
# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("L-H","Trackbars",0,255,nothing)
# cv2.createTrackbar("L-S","Trackbars",0,255,nothing)
# cv2.createTrackbar("L-V","Trackbars",0,255,nothing)
# cv2.createTrackbar("U-H","Trackbars",0,255,nothing)
# cv2.createTrackbar("U-S","Trackbars",0,255,nothing)
# cv2.createTrackbar("U-V","Trackbars",0,255,nothing)
#videowrite
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 10.0, (640,480))
timeElapsedlist = []
while True:
    ret, image=cam.read()
    startTime = time.time()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    frame = cv2.flip(thresh,1)
        # write the flipped frame
#     l_h = cv2.getTrackbarPos("L-H","Trackbars")
#     l_s = cv2.getTrackbarPos("L-S","Trackbars")
#     l_v = cv2.getTrackbarPos("L-V","Trackbars")
#     u_h = cv2.getTrackbarPos("U-H","Trackbars")
#     u_s = cv2.getTrackbarPos("U-S","Trackbars")
#     u_v = cv2.getTrackbarPos("U-V","Trackbars")
    hsv_img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
#     # create the Mask
#     lower_range = np.array([l_h,l_s,l_v])
#     upper_range = np.array([u_h,u_s,u_v])
    lower_range = np.array([55,100,100])
    upper_range = np.array([86,255,255])
    mask = cv2.inRange(hsv_img, lower_range, upper_range)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        (x,y),radius = cv2.minEnclosingCircle(all_contour_points)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(image, (cX, cY), 15, (0,0,255), 8)     
    cv2.imshow("cam",image)
    out.write(image)
    timeElapsed = time.time() - startTime 
    timeElapsedlist.append(timeElapsed)
    # open .txt file to save data
    f = open('hw3data.txt','a')
    # print time to run through loop to the screen & save to file
    f.write(str(timeElapsed))
    f.write('\n')
    print('time elapsed in this frame is > > > > ', timeElapsed)
    k = cv2.waitKey(100) & 0xFF
    if k == 27: 
        break
f.close()
cam.release()
out.release()
cv2.destroyAllWindows()
