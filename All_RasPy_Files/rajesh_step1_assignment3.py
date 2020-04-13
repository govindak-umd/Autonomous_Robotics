import cv2
frame = cv2.imread("rajesh.jpg")


# In[2]:


hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


# In[6]:


import numpy as np
lower_green = np.array([36, 25, 25])
upper_green = np.array([70, 255,255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_green, upper_green)
img,contours,hierachy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(frame, contours, -1, (0,0,255), 3)
# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame,frame, mask= mask)


cv2.imshow('frame',frame)
cv2.imwrite("Rajesh_sign.jpg",frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('mask',mask)
cv2.imwrite("Rajesh_mask.jpg",mask)
cv2.waitKey(0)
cv2.imwrite("Rajesh_res.jpg",res)
cv2.destroyAllWindows()
cv2.imshow('res',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
#k = cv2.waitKey(5) & 0xFF
#if k == 27:
    #cv2.destroyAllWindows()