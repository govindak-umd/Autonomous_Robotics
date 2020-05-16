#!/usr/bin/env python
# coding: utf-8

# # Step: 1

# In[1]:


import numpy as np
import cv2 # OpenCV-Python
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import imutils
import time


# In[2]:


img = cv2.imread('orange_final.jpg',1) 

if img is None:
    print ('Open Error')
else:
    print ('Image Loaded')
img = imutils.resize(img, width=500) #justto beable to see clearly
cv2.imshow('NORMAL IMAGE',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


# In[3]:


hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow('HSV IMAGE',hsv_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[69]:


img.shape


# In[70]:


img.shape[0:2]


# In[71]:


img[:,:,2]


# In[72]:


blank_canvas = np.zeros((1347, 1230,3),np.uint8)


# In[73]:


plt.imshow(blank_canvas)


# In[4]:


lower_range = np.array([0, 49, 169])
upper_range = np.array([179, 255, 255])


# In[5]:


blank_canvas = cv2.inRange(hsv_img, lower_range, upper_range)


# In[6]:


cv2.imshow('Blank canvas', blank_canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[7]:


blank_canvas.shape


# In[8]:


edged = cv2.Canny(blank_canvas, 30, 200) 
cv2.waitKey(0) 


# In[9]:


contours, hierarchy = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 


# In[10]:


# contours


# In[11]:


cv2.imshow('Canny Edges After Contouring', edged)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[12]:


print("Number of Contours found = " + str(len(contours))) 


# In[13]:


cv2.drawContours(blank_canvas, contours, -1, (0, 255, 0), 3) 


# In[14]:


cv2.imshow('Contours', blank_canvas) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 


# In[15]:


combined = np.hstack((img[:,:,1],hsv_img[:,:,1],blank_canvas))


# In[16]:


cv2.imshow('combined', combined) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 


# # Step: 2

# In[17]:


all_contour_points = contours[0]


# In[18]:


(x,y),radius = cv2.minEnclosingCircle(all_contour_points)
center = (int(x),int(y))
r = int(radius)
cv2.circle(img,center,r,(0,255,0),3)
cv2.circle(img,center,3,(255,255,0),3)
cv2.drawContours(img, [all_contour_points], 0, (0,0,255), 3)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# # Step: 3

# # Tracking the video

# In[19]:


#https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
import numpy as np
import cv2 # OpenCV-Python
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import imutils
import time

def nothing(x):
    pass

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
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
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
    lower_range = np.array([0,49,169])
    upper_range = np.array([179,255,255])
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
        cv2.circle(image, (cX, cY), radius, (0,0,255), 8)     
    cv2.imshow("cam",image)
    out.write(image)
    timeElapsed = time.time() - startTime 
    timeElapsedlist.append(timeElapsed)
    blank_canvas = cv2.inRange(hsv_img, lower_range, upper_range)
    cv2.imshow("blank_canvas",blank_canvas)
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


# In[106]:


timeElapsedlist = []
#opening the text file and extracting the 5th column
with open('hw3data.txt') as f: 
    for line in f:
        timeElapsedlist.append(float(line[0:15]))
#         count= count + 1 #incrementing count


# In[100]:


timeElapsedlist


# In[108]:


timeElapsed = np.array(timeElapsedlist)


# In[109]:


length_of_time = len(timeElapsedlist)


# # Graph 1

# In[110]:


x = np.linspace(1,len(timeElapsedlist),len(timeElapsedlist))
y = timeElapsedlist
plt.figure(1)
plt.plot(x,y,color='r',linewidth=1.0,label='Raw data') #plotting
plt.title('Object Tracking Processing Time') #assigning plot title
plt.xlabel('Frame') #assigning x label
plt.ylabel('Processing time [msec]') #assigning y label
plt.legend(loc="upper right")#assigning legend and position of the legend
plt.show() #showing the plot


# # Graph 2

# In[111]:


plt.figure(2)
plt.title('Object Tracking Processing Time') #assigning plot title
plt.xlabel('Processing time [msec]') #assigning x label
plt.ylabel('Frame') #assigning y label
x = timeElapsedlist
num_bins = len(timeElapsedlist)
n, bins, patches = plt.hist(x, num_bins, facecolor='k', alpha=0.5)
plt.show()


# In[ ]:




