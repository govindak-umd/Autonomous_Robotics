#Importing the Libraries
import numpy as np
import cv2 # OpenCV-Python
import matplotlib.pyplot as plt
import imutils
import time

img = cv2.imread("govind.jpg") #reading the image

if img is None: #for error checking
    print ('Open Error')
else:
    print ('Image Loaded') 
img = imutils.resize(img, width=500) #justto beable to see clearly #resizing the image
cv2.imshow('NORMAL IMAGE',img) #showing the image
cv2.waitKey(0)
cv2.destroyAllWindows()

hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #converting to HSV format
cv2.imshow('HSV IMAGE',hsv_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

lower_range = np.array([36, 25, 25]) #lower range of HSV
upper_range = np.array([70, 255, 255]) #lower range of HSV

blank_canvas = cv2.inRange(hsv_img, lower_range, upper_range) #BLANK CANVAS is the mask here

cv2.imshow('Blank canvas', blank_canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()

edged = cv2.Canny(blank_canvas, 30, 200)   #using the canny edge detector
img,contours,hierachy = cv2.findContours(blank_canvas,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) #finding the contours
cv2.imshow('Canny Edges After Contouring', edged) 
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Number of Contours found = " + str(len(contours)))  #determining the total contours that have been found

cv2.drawContours(blank_canvas, contours, -1, (0, 255, 0), 3) #drawing the contours

cv2.imshow('Contours', blank_canvas) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 

print(' printing contours .. ')
print(contours)
all_contour_points = contours[0] 

(x,y),radius = cv2.minEnclosingCircle(all_contour_points)#drawing the minimum enclosed circle
center = (int(x),int(y)) #determining the center of the circle
r = int(radius) #radius of the circle
cv2.circle(img,center,r,(0,255,0),3) 
cv2.circle(img,center,3,(255,255,0),3)
cv2.drawContours(img, [all_contour_points], 0, (0,0,255), 3) #drawing the contours
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Capturing the Video using the Pi-cam
cam= cv2.VideoCapture(0)
fps = cam.get(cv2.CAP_PROP_FPS)
timestamps = [cam.get(cv2.CAP_PROP_POS_MSEC)] #to obtain the timestamps
calc_timestamps = [0.0]
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 10.0, (640,480)) #determining the output video characteristics
timeElapsedlist = [] 
while True:
    ret, image=cam.read()
    startTime = time.time()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converting to a grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) #blurring the frame
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1] #the threshold
    frame = cv2.flip(thresh,1) #flipping the frame, to account for any rotation
    hsv_img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) #converting to hsv image format
    lower_range = np.array([55,100,100])# create the Mask's lower HSV Range
    upper_range = np.array([86,255,255])# create the Mask's Upper HSV Range
    mask = cv2.inRange(hsv_img, lower_range, upper_range) #developing the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #finding the contours
    cnts = imutils.grab_contours(cnts) #grabbing all the contours
    for c in cnts:
        M = cv2.moments(c) #cv2.moments for the center
        if M["m00"] != 0: 
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        (x,y),radius = cv2.minEnclosingCircle(all_contour_points)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(image, (cX, cY), 15, (0,0,255), 8)   #drawing the circle in the vide
    cv2.imshow("cam",image)
    out.write(image)
    timeElapsed = time.time() - startTime  #calculating the elapsed time
    timeElapsedlist.append(timeElapsed) #appending to the time-list
    # open .txt file to save data
    f = open('hw3data.txt','a')#saving the data of the hardware limitation to a text file, named hw3data.txt
    # print time to run through loop to the screen & save to file
    f.write(str(timeElapsed)) 
    f.write('\n')
    print('time elapsed in this frame is > > > > ', timeElapsed)#printing out the time elapsed
    k = cv2.waitKey(100) & 0xFF
    if k == 27: 
        break
f.close()
cam.release() #releasing the video
out.release() 
cv2.destroyAllWindows()#safely closing all the windows
