import RPi.GPIO as GPIO
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import imutils
import os
import matplotlib.pyplot as plt
trig = 16
echo = 18
servo = 36
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo,GPIO.OUT)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(31,GPIO.OUT) #IN1
GPIO.setup(33,GPIO.OUT) #IN2
GPIO.setup(35,GPIO.OUT) #IN3
GPIO.setup(37,GPIO.OUT) #IN4
pwm = GPIO.PWM(servo,40)
pwm.start(9.7)
time.sleep(1)
i = 0

def gameover():
    GPIO.output(31,False)
    GPIO.output(33,False)
    GPIO.output(35,False)
    GPIO.output(37,False)
    
def forward(tf):
    GPIO.output(31,True)
    
    GPIO.output(33,False)
    
    GPIO.output(35,False)
    
    GPIO.output(37,True)
    time.sleep(tf)
    gameover()
    
def reverse(tf):

    GPIO.output(31,False)
    
    GPIO.output(33,True)
    
    GPIO.output(35,True)
    
    GPIO.output(37,False)
    time.sleep(tf)
    gameover()
    
def right(tf):

    GPIO.output(31,True)
    
    GPIO.output(33,False)
    
    GPIO.output(35,True)
    
    GPIO.output(37,False)

    time.sleep(tf)
    gameover()
    
def left(tf):
    
    GPIO.output(31,False)
    
    GPIO.output(33,True)
    GPIO.output(35,False)
    
    GPIO.output(37,True)
    time.sleep(tf)
    gameover()
    
def key_input(event):
    init()
    print("Key=", event)
    tf=1
    if(key_press.lower()=='w'):
        forward(tf)
    elif(key_press.lower()=='z'):
        reverse(tf)
    elif(key_press.lower()=='a'):
        left(tf)
    elif(key_press.lower()=='s'):
        right(tf)
    else:
        print("Invalid key pressed")



def calc_distance():
    #defining the board layout
    
    #ensure that the output has no value
    GPIO.output(trig,False)
    time.sleep(0.010)

    #generate the trigger pulse
    GPIO.output(trig,True)
    time.sleep(0.00001) #this is 10 microseconds
    GPIO.output(trig,False)
    #all_distance=[]
    #generating the return / echo signals
    while GPIO.input(echo)==0:
        pulse_start=time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start

    #convert time to distance

    distance = pulse_duration*17150
    distance = round(distance,2)
    #all_distance.append(distance)
    time.sleep(1)
    #cleanup gpio pins and 
    return(distance)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 45
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    # show the frame
    image = cv2.flip(image,0)
    image = cv2.flip(image,1)
    distance = calc_distance()
    if 0<=distance<=8.5:
        pwm.ChangeDutyCycle(6.0)
    
    #pwm.ChangeDutyCycle(9.7)
    pwm.ChangeDutyCycle(6.0)
    pwm.ChangeDutyCycle(6.0)
    pwm.ChangeDutyCycle(6.0)
    pwm.ChangeDutyCycle(6.0)
    cv2.putText(image,'distance :'+str(distance),(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
    cv2.imshow("Frame", image)
#     time.sleep(1)
    
#     time.sleep(0.4)
#     pwm.ChangeDutyCycle(6.0)
#     time.sleep(0.4)
    
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        cv2.destroyAllWindows()
        pwm.stop()
        GPIO.cleanup()
        break


