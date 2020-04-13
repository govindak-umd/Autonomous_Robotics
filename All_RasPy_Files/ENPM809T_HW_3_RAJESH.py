#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2


# In[2]:


import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_green = np.array([36, 25, 25])
    upper_green = np.array([70, 255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()


# In[1]:


import cv2
frame = cv2.imread(r"C:\Users\nsraj\Pictures\traffic_img.png")


# In[2]:


hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


# In[6]:


import numpy as np
lower_green = np.array([36, 25, 25])
upper_green = np.array([70, 255,255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_green, upper_green)
contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(frame, contours, -1, (0,0,255), 3)
# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame,frame, mask= mask)


cv2.imshow('frame',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('mask',mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('res',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
#k = cv2.waitKey(5) & 0xFF
#if k == 27:
    #cv2.destroyAllWindows()


# In[6]:


import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([36, 25, 25])
    upper_blue = np.array([70, 255,255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1)
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()

