import numpy as np
import cv2 # OpenCV-Python
import matplotlib.pyplot as plt
import imutils
import time
import RPi.GPIO as gpio
import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import serial
ser = serial.Serial('/dev/ttyUSB0',9600)
imu_data = []
#email
def email_Send():
    pic_time = datetime.now().strftime('%Y%m%d%H%M%S')
#     command = 'raspistill -w 1280 -h 720 -vf -hf -o ' + pic_time + '.jpg'
#     os.system(command)

    #EMAIL
    smtpUser = 'enpm809tslamdunk@gmail.com'
    smtpPass = 'pi@slamdunk'

    #DESTINATION
    toAdd = 'govindajithkumar97@gmail.com'
    fromAdd = smtpUser
    subject = 'IMAGE RECORDED FROM PI' + pic_time
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromAdd
    msg['To'] = toAdd
    msg.preamble = "IMage recorded at : " + pic_time

    #EMAIL TEXT
    body = MIMEText("Image recorded at : " + pic_time)
    msg.attach(body)
    
    fp = open('email_image_captured'+'.png','rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    #send email

    s = smtplib.SMTP('smtp.gmail.com',587)

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(smtpUser,smtpPass)
    s.sendmail(fromAdd, toAdd, msg.as_string())
    s.quit()

    print("Email DELIVERED!!!!!")

gpio.setmode(gpio.BOARD)
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
    

    
init()

pin1 = 33
pin2 = 37
pwm1 = gpio.PWM(pin1,50)
pwm2 = gpio.PWM(pin2,50)

pin3 = 31
pin4 = 35
pwm3 = gpio.PWM(pin3,50)
pwm4 = gpio.PWM(pin4,50)
val = 60
val_f = 70

#servo
gpio.setup(36,gpio.OUT)
pwm = gpio.PWM(36,50)
#####    
def forward(val_f):
    pwm3.start(val_f)
    pwm2.start(val_f)
    time.sleep(0.1)

def reverse(val_f):
    pwm1.start(val_f)
    pwm4.start(val_f)
    time.sleep(0.1)
      
def left(val):
    pwm1.start(val)
    pwm2.start(val)
    time.sleep(0.1)
    
def right(val):
    pwm3.start(val)
    pwm4.start(val)
    time.sleep(0.1)
    
def stop():
    pwm1.stop()
    pwm2.stop()
    pwm3.stop()
    pwm4.stop()
    time.sleep(0.1)
pwm.start(8.3)
def servo_open():
    
    time.sleep(0.1)
    i = 0
    for i in range(5):
        pwm.ChangeDutyCycle(12.0)
        time.sleep(0.1)
#     pwm.stop()
    
def servo_close():
#     pwm.start(8.3)
    time.sleep(0.1)
    i = 0
    for i in range(5):
        pwm.ChangeDutyCycle(6.5)
        time.sleep(1)
#     pwm.stop()


trig = 16
echo = 18

def Ultrasonic_distance():
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
    try:
        while gpio.input(echo)==0:
            pulse_start=time.time()
        while gpio.input(echo) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        #convert time to distance
        distance = pulse_duration*17150
        distance = round(distance,2)
    except:
        distance = 999 #arbitary high value > 9, because of the ultrasonic threshold mentioned below.
    return(distance)




cam= cv2.VideoCapture(0)
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
flag = False #for opening
flag2 = False # for closing
while True:      
    line = ser.readline()
    line = line.rstrip().lstrip()
    line = str(line)
    line = line.strip("'")
    line = line.strip("b'")
    imu_data.append(line)
    print("imu=",line)
    dist_US = Ultrasonic_distance()
    if dist_US>9 and flag == False:
        print('SERVO OPENING')
        servo_open()
        time.sleep(0.8)
        
        flag = True
        flag2 = False
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
        print('------- horizontal distance ------ ' , dist_2)
        cv2.putText(orig_image,'Ultrasonic : '+str(dist_US),(10,440),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2,cv2.LINE_AA)
        draw(orig_image)
        cv2.putText(orig_image,'Centre point offset : ' + str(dist_2),(10,410),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),2,cv2.LINE_AA)

        if(dist_2<-50):
            print(' turning right ONLY')
            right(val)
            
        elif(dist_2>50):
            print(' turning left ONLY')
            left(val)
            
        elif(-50<=dist_2<=50):
            dist_US = Ultrasonic_distance()
            print( ' dist_US WHILE MOVING STRAIGHT >>>>>>>> ' , dist_US)
            if dist_US>9:
                forward(val_f)
            stop()
            if dist_US<=9and flag2 == False:
                print('SERVO CLOSING')
                cv2.putText(orig_image,'Email sent regarding object pickup to Dr. M',(10,30),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),2,cv2.LINE_AA)
                cv2.imwrite ('email_image_captured.png',orig_image)
                print('writing image ' )
                #time.sleep(0.5)
                email_Send()
                servo_close()
                time.sleep(1.5)
#                 time.sleep(3)
                print('CLOSING COMPLETE')
                flag2 = True
                print('reversing now')
                reverse(val_f)
                time.sleep(3.5)
                stop()
                print('servo opening again')
                servo_open()
                time.sleep(0.8)
                reverse(val_f)
                time.sleep(1)
                left(val)
                time.sleep(2)
                forward(val_f)
                time.sleep(1)
                
            

        

    except:
        stop()
        print('ERROR OCCURED')
        pass
    
    cv2.imshow("contour image",orig_image)
#     cv2.imshow("mask",mask)
    cv2.imwrite (str(count+100)+'.png',orig_image)
#     out.write(orig_image)

    count+=1
    k = cv2.waitKey(100) & 0xFF
    if k == 27: 
        break
file = open('assignment_9_imu_values.txt','w')
for i in imu_data:
    file.write(str(i))
    file.write('\n')
file.close()
gameover()
gpio.cleanup()
cam.release()
# out.release()
cv2.destroyAllWindows()



