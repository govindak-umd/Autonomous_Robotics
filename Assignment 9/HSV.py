import numpy as np
import cv2 # OpenCV-Python
import matplotlib.pyplot as plt
import imutils
import time
import RPi.GPIO as gpio

def init():

    gpio.setup(31,gpio.OUT) #IN1
    gpio.setup(33,gpio.OUT) #IN2
    gpio.setup(35,gpio.OUT) #IN3
    gpio.setup(37,gpio.OUT) #IN4

def gameover():
    gpio.output(31,False)
    gpio.output(33,False)
    gpio.output(35,False)
    gpio.output(37,False)

gpio.setmode(gpio.BOARD)
    
init()

pin1 = 33
pin2 = 37
pwm1 = gpio.PWM(pin1,50)
pwm4 = gpio.PWM(pin2,50)

pin3 = 31
pin4 = 35
pwm2 = gpio.PWM(pin3,50)
pwm3 = gpio.PWM(pin4,50)
val = 61
def left(val):
    pwm1.start(val)
    pwm4.start(val)
#     gameover()
    time.sleep(0.1)
    
def right(val):
    pwm2.start(val)
    pwm3.start(val)
#     gameover()
    time.sleep(0.1)
    
def stop():
   
    pwm1.stop()
    pwm2.stop()
    pwm3.stop()
    pwm4.stop()
    time.sleep(0.1)

cam= cv2.VideoCapture(0)
# fps = cam.get(cv2.CAP_PROP_FPS)
# timestamps = [cam.get(cv2.CAP_PROP_POS_MSEC)]
# calc_timestamps = [0.0]
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('hsvassignment9.avi', fourcc, 1.0, (int(cam.get(3)),int(cam.get(4))))
count=0
def calc_dist(pt1):
    pt2 = (320,240)
    dist = 320-pt1[0]
    return dist

def draw(orig_image):
    cv2.line(orig_image,(320,0),(320,480),(255,255,255),1)
    cv2.line(orig_image,(0,240),(640,240),(255,255,255),1)
    cv2.circle(orig_image,(centre_x,centre_y),100,(0,255,0),2)
    cv2.circle(orig_image,(centre_x,centre_y),4,(255,255,255),-1)
while True:
    ret, image=cam.read()
    image = cv2.flip(image,-1)
    orig_image = image
    hsv_img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_range = np.array([0,105,175])
    upper_range = np.array([180,255,255])
    mask = cv2.inRange(hsv_img, lower_range, upper_range)
    edged = cv2.Canny(mask, 30, 200)
    try:
        _,contours,_= cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours_poly = [None]*len(contours)
        centers = [None]*len(contours)
        radius = [None]*len(contours)
        cx= []
        cy = []
        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
            cx.append(centers[i][0])
            cy.append(centers[i][1])
        centre_x= int((min(cx)+max(cx))/2)
        centre_y = int((min(cy)+max(cy))/2)
        dist_2 = calc_dist((centre_x,centre_y))
        
        
        if(dist_2<-100):
            right(val)
            
        elif(dist_2>100):
            left(val)
            
        elif(-100<=dist_2<=100):
            stop()
            
            
        print("dist_2",dist_2)
        
        draw(orig_image)
        cv2.putText(orig_image,str(dist_2),(500,240),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),2,cv2.LINE_AA)
    except:
        pass
    
    cv2.imshow("contour image",orig_image)
#     out.write(orig_image)
    cv2.imwrite(str(count)+'.png',orig_image)
    count+=1
    k = cv2.waitKey(100) & 0xFF
    if k == 27: 
        break
gameover()
gpio.cleanup()
cam.release()
# out.release()
cv2.destroyAllWindows()


