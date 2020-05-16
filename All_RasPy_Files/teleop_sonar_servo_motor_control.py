import RPi.GPIO as gpio
import time
import datetime
import os
import glob
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

trig = 16
echo = 18
servo = 36
gpio.setmode(gpio.BOARD)
gpio.setup(servo,gpio.OUT)
gpio.setup(trig,gpio.OUT)
gpio.setup(echo,gpio.IN)

gpio.setup(31,gpio.OUT) #IN1
gpio.setup(33,gpio.OUT) #IN2
gpio.setup(35,gpio.OUT) #IN3
gpio.setup(37,gpio.OUT)

pwm = gpio.PWM(servo,50)
pwm.start(7.0)

i = 0
distance = 0
list_of_images = {} 
def calc_distance():
    #defining the board layout
    
    #ensure that the output has no value
    gpio.output(trig,False)
    time.sleep(0.010)

    #generate the trigger pulse
    gpio.output(trig,True)
    time.sleep(0.00001) #this is 10 microseconds
    gpio.output(trig,False)
    while gpio.input(echo)==0:
        pulse_start=time.time()
    while gpio.input(echo) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration*17150
    distance = round(distance,2)

    return(distance)
    
def gameover():
    gpio.output(31,False)
    gpio.output(33,False)
    gpio.output(35,False)
    gpio.output(37,False)
    
def forward(tf):
    gpio.output(31,True)
    
    gpio.output(33,False)
    
    gpio.output(35,False)
    
    gpio.output(37,True)

    time.sleep(tf)
    gameover()

    
def reverse(tf):
    gpio.output(31,False)
    
    gpio.output(33,True)
    
    gpio.output(35,True)
    
    gpio.output(37,False)

    time.sleep(tf)
    gameover()

    
def right(tf):
    gpio.output(31,True)
    
    gpio.output(33,False)
    
    gpio.output(35,True)
    
    gpio.output(37,False)

    time.sleep(tf)
    gameover()

def left(tf):

    
    gpio.output(31,False)
    
    gpio.output(33,True)
    gpio.output(35,False)
    
    gpio.output(37,True)

    time.sleep(tf)
    gameover()



def key_input(event):

    print("Key=", event)
    tf= 0.5
    if(key_press.lower()=='w'):
        forward(tf)
    elif(key_press.lower()=='s'):
        reverse(tf)
    elif(key_press.lower()=='a'):
        left(tf)
    elif(key_press.lower()=='d'):
        right(tf)
    elif(key_press.lower()=='o'):
        pass
    elif(key_press.lower()=='c'):
        pass
    elif(key_press.lower()=='x'):
        pass
    else:
        print("INVALID key pressed")

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 5.0, (640,480))
# capture frames from the
counter = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if counter ==0:
        pwm.ChangeDutyCycle(7.0)
        time.sleep(0.3)
    image = frame.array
    image = cv2.flip(image,0)
    image = cv2.flip(image,1)
    dist = calc_distance()
    if dist<7:
        pwm.ChangeDutyCycle(3.5)
        time.sleep(0.3)
    cv2.putText(image,'distance is ' + str(dist),(100,100),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),1,cv2.LINE_AA)
    out.write(image)
    if counter%2 == 0:
        key_press = input("Enter direction:")
        if key_press == 'o':
            pwm.ChangeDutyCycle(7.0)
            time.sleep(0.3)
        elif key_press == 'c':
            pwm.ChangeDutyCycle(2.5)
            time.sleep(0.3)
        if key_press == 'x':
            pwm.ChangeDutyCycle(7.0)
            time.sleep(1)
            pwm.stop()
            gpio.cleanup()
            break
    key_input(key_press)  
    rawCapture.truncate(0)
    counter+=1
    # clear the stream in preparation for the next frame
out.release()
cv2.destroyAllWindows()