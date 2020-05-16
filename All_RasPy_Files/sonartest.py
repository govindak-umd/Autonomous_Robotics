import RPi.GPIO as gpio
import time
import cv2
import numpy as np
import imutils
import os
import matplotlib.pyplot as plt

name = "sonartestimage.jpg"
os.system('raspistill -w 640 -h 480 -o '  + name)

#Define Pin allocation
trig = 16
echo = 18

def distance():
    #defining the board layout
    gpio.setmode(gpio.BOARD)
    gpio.setup(trig,gpio.OUT)
    gpio.setup(echo,gpio.IN)
    #ensure that the output has no value
    gpio.output(trig,False)
    time.sleep(0.010)

    #generate the trigger pulse
    gpio.output(trig,True)
    time.sleep(0.00001) #this is 10 microseconds
    gpio.output(trig,False)
    all_distance=[]
    #generating the return / echo signals
    while gpio.input(echo)==0:
        pulse_start=time.time()
    while gpio.input(echo) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start

    #convert time to distance

    distance = pulse_duration*17150
    distance = round(distance,2)
    all_distance.append(distance)
    #time.sleep(1)
    gpio.cleanup()
    #cleanup gpio pins and 
    return(distance)
while True:
    dist = distance()
    print("dist=",dist)
# all_distance=[]
# for i in range(10):
#     print("distance: ",distance(),"cm")
#     all_distance.append(distance())
#     time.sleep(0.1)
#     
# print('all distances are : ',all_distance)
#  
# sum=0.00
# for i in range(len(all_distance)):
#     sum = sum+all_distance[i]
# mean_value = float(sum/10)
# print('The mean distance is : ',mean_value)
# 
# # Read the image
# img = cv2.imread('sonartestimage.jpg')
# # initialize counter
# print(img.shape)
# 
# while True:
#     # Display the image
# #    cv2.imshow('a',img)
#     # wait for keypress
#     k = cv2.waitKey(0)
#     # specify the font and draw the key using puttext
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     cv2.putText(img,'mean :'+str(mean_value),(100,100), font,1,(255,255,255),1,cv2.LINE_AA)
#     cv2.imshow('a',img)
#     plt.savefig('sonar_submission.png')
#     if k == ord('q'):
#         break
# cv2.destroyAllWindows()






















