#!/usr/bin/env python
# coding: utf-8

# In[1]:


#IMPORTING LIBRARIES
import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils
import time


# In[2]:


img = cv2.imread('samp.jpg',1)#reading the arrow image
cv2.imshow('Me with the Green Arrow',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[3]:


#CONVERTING TO HSV IMAGE
hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow('HSV IMAGE',hsv_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[4]:


#FORMING BLANK CANVAS OF THE SAME DIMENSIONS
h = img.shape[0]
w = img.shape[1]
blank_canvas = np.zeros((h,w,3),np.uint8) #creating the blank canvas


# In[5]:


cv2.imshow('blank_canvas',blank_canvas) #serves as the HSV mask
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[6]:


#setting the range for the hsv
lower_range = np.array([0, 117, 177]) #lower range of HSV
upper_range = np.array([255, 255, 255]) #lower range of HSV


# In[7]:


#SHOWING THE MASKED HSV 
hsv_masked_to_green_only = cv2.inRange(hsv_img, lower_range, upper_range)


# In[8]:


cv2.imshow('hsv_masked_to_green_only',hsv_masked_to_green_only)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[9]:


#CONDUCTING GAUSSIAN BLUR
blur = cv2.GaussianBlur(hsv_masked_to_green_only,(11,11),0)


# In[10]:


cv2.imshow('blur',blur)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[11]:


#SHI TOMASI CORNER DETECTION
corners = cv2.goodFeaturesToTrack(blur,7,0.01,10)
corners = np.int0(corners)
all_x =[]
all_y= []
img2 = img.copy()
#DISPLAYING THE CORNERS ON THE ORIGINAL IMAGE
for i in corners:
    x,y = i.ravel()
    all_x.append(x)
    all_y.append(y)
    cv2.circle(img2,(x,y),7,255,-1)
    cv2.putText(img2,'('+str(x)+','+str(y)+')',(x,y),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255),2)
diff_x = max(all_x) - min(all_x) #checking the distance between x points MAX- MIN
diff_y = max(all_y) - min(all_y)#checking the distance between y points MAX- MIN
mid_x = min(all_x) + (diff_x/2)
mid_y = min(all_y) + (diff_y/2)


# In[12]:


#SHOWING THE IMAGE WITH THE CORNERS
cv2.imshow('Points on the arrow',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[13]:


#DECIDING THE DIRECTIONS

if diff_x>diff_y: #could be west or east
    num_of_points_greater_x = []
    num_of_points_lesser_x = []
    for i in all_x:
        if i>mid_x:
            num_of_points_greater_x.append(1)
        else:
            num_of_points_lesser_x.append(1)
    if len(num_of_points_greater_x)>len(num_of_points_lesser_x):
        cv2.putText(img2,'EAST',(100,100),cv2.FONT_HERSHEY_DUPLEX,3,(255,255,255),2)
    else:
        cv2.putText(img2,'WEST',(100,100),cv2.FONT_HERSHEY_DUPLEX,3,(255,255,255),2)
else: #could be north or south
    num_of_points_greater_y = []
    num_of_points_lesser_y = []
    for i in all_y:
        if i>mid_y:
            num_of_points_greater_y.append(1)
        else:
            num_of_points_lesser_y.append(1)
    if len(num_of_points_greater_y)>len(num_of_points_lesser_y):
        cv2.putText(img2,'SOUTH',(100,100),cv2.FONT_HERSHEY_DUPLEX,3,(255,255,255),2)
    else:
        cv2.putText(img2,'NORTH',(100,100),cv2.FONT_HERSHEY_DUPLEX,3,(255,255,255),2)


# In[14]:


cv2.imshow('Final Direction',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[ ]:





# In[15]:


#Video code
#Capturing the Video using the Pi-cam
cam= cv2.VideoCapture(0)
fps = cam.get(cv2.CAP_PROP_FPS)
timestamps = [cam.get(cv2.CAP_PROP_POS_MSEC)] #to obtain the timestamps
calc_timestamps = [0.0]
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('fourthassignment.avi', fourcc, 10.0, (640,480)) #determining the output video characteristics
timeElapsedlist = [] 
def nothing(x):
    pass
#cv2.namedWindow("Trackbars")
#cv2.createTrackbar("L-H","Trackbars",0,255,nothing)
#cv2.createTrackbar("L-S","Trackbars",0,255,nothing)
#cv2.createTrackbar("L-V","Trackbars",0,255,nothing)
#cv2.createTrackbar("U-H","Trackbars",0,255,nothing)
#cv2.createTrackbar("U-S","Trackbars",0,255,nothing)
#cv2.createTrackbar("U-V","Trackbars",0,255,nothing)
while True:
    ret, img=cam.read()
    startTime = time.time()
    #CONVERTING TO HSV IMAGE
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#     cv2.imshow('HSV IMAGE',hsv_img)
    #FORMING BLANK CANVAS OF THE SAME DIMENSIONS
    h = img.shape[0]
    w = img.shape[1]
    blank_canvas = np.zeros((h,w,3),np.uint8) #creating the blank canvas
    #setting the range for the hsv
        # write the flipped frame
#    l_h = cv2.getTrackbarPos("L-H","Trackbars")
 #   l_s = cv2.getTrackbarPos("L-S","Trackbars")
  #  l_v = cv2.getTrackbarPos("L-V","Trackbars")
  #  u_h = cv2.getTrackbarPos("U-H","Trackbars")
  #  u_s = cv2.getTrackbarPos("U-S","Trackbars")
  #  u_v = cv2.getTrackbarPos("U-V","Trackbars")
    lower_range = np.array([0, 117, 177]) #lower range of HSV
    upper_range = np.array([255, 255, 255]) #lower range of HSV
    # create the Mask
#    lower_range = np.array([l_h,l_s,l_v])
 #   upper_range = np.array([u_h,u_s,u_v])
    #SHOWING THE MASKED HSV 
    hsv_masked_to_green_only = cv2.inRange(hsv_img, lower_range, upper_range)
#     cv2.imshow('hsv_masked_to_green_only',hsv_masked_to_green_only)
    #CONDUCTING GAUSSIAN BLUR
    blur = cv2.GaussianBlur(hsv_masked_to_green_only,(11,11),0)
    #SHI TOMASI CORNER DETECTION
    corners = cv2.goodFeaturesToTrack(blur,7,0.01,10)
    corners = np.int0(corners)
    all_x =[]
    all_y= []
    img2 = img.copy()
    #DISPLAYING THE CORNERS ON THE ORIGINAL IMAGE
    for i in corners:
        x,y = i.ravel()
        all_x.append(x)
        all_y.append(y)
        cv2.circle(img2,(x,y),7,25,-1)
       # cv2.putText(img2,'('+str(x)+','+str(y)+')',(x,y),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255),2)
    diff_x = max(all_x) - min(all_x) #checking the distance between x points MAX- MIN
    diff_y = max(all_y) - min(all_y)#checking the distance between y points MAX- MIN
    mid_x = min(all_x) + (diff_x/2)
    mid_y = min(all_y) + (diff_y/2)
    #DECIDING THE DIRECTIONS

    if diff_x>diff_y: #could be west or east
        num_of_points_greater_x = []
        num_of_points_lesser_x = []
        for i in all_x:
            if i>mid_x:
                num_of_points_greater_x.append(1)
            else:
                num_of_points_lesser_x.append(1)
        if len(num_of_points_greater_x)>len(num_of_points_lesser_x):
            cv2.putText(img2,'RIGHT',(100,100),cv2.FONT_HERSHEY_DUPLEX,3,(255,0,255),2)
        else:
            cv2.putText(img2,'LEFT',(100,100),cv2.FONT_HERSHEY_DUPLEX,3,(255,0,255),2)
    else: #could be north or south
        num_of_points_greater_y = []
        num_of_points_lesser_y = []
        for i in all_y:
            if i>mid_y:
                num_of_points_greater_y.append(1)
            else:
                num_of_points_lesser_y.append(1)
        if len(num_of_points_greater_y)>len(num_of_points_lesser_y):
            cv2.putText(img2,'DOWN',(100,100),cv2.FONT_HERSHEY_DUPLEX,3,(255,0,255),2)
        else:
            cv2.putText(img2,'UP',(100,100),cv2.FONT_HERSHEY_DUPLEX,3,(255,0,255),2)
    cv2.imshow('Final Direction',img2)
    out.write(img2)
    timeElapsed = time.time() - startTime  #calculating the elapsed time
    timeElapsedlist.append(timeElapsed) #appending to the time-list
    # open .txt file to save data
    f = open('hw4data.txt','a')#saving the data of the hardware limitation to a text file, named hw3data.txt
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


# In[ ]:




