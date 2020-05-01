#automatically rotate the wheel for one rotation and test the encoder
import RPi.GPIO as gpio
import time
import numpy as np
import serial


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

#MAIN CODE
#right back wheel encoder
gpio.setup(12,gpio.IN,pull_up_down = gpio.PUD_UP)
#left front wheel encoder
gpio.setup(7,gpio.IN,pull_up_down = gpio.PUD_UP)




#initialize pwm signal to control motor
angle = 90 #USER DEFINED ANGLE
time_left_turn  = ((angle*1.3)/90)

list_of_gpio = []
list_of_gpio_2 = []
list_of_x = []
def forward(time_to_run,ser):
    pin = 31
    pin2 = 37
    val = 30
    pwm1 = gpio.PWM(pin,50)
    pwm1.start(val)
    pwm4 = gpio.PWM(pin2,50)
    pwm4.start(val)
    t = time.time()
    counter = np.uint64(0)
    counter2 = np.uint64(0) 
    button = int(0)
    button2 = int(0)
    while time.time()-t<time_to_run:
        #time.sleep(0.1)
        line = ser.readline()
        print('LINE', line)
        line = line.rstrip().lstrip()
            #print(line)
            
        line = str(line)
        line = line.strip("'")
        line = line.strip("b'")
        print("imu=",line)
        list_of_x.append(line[3:])
        if int (gpio.input(12)) != int(button):
            button = int(gpio.input(12))
            counter+= 1
        if int (gpio.input(7)) != int(button2):
            button2 = int(gpio.input(7))
            counter2+=1
            
        #PROPORTIONAL CONTROLLER
        err = counter - counter2
        print(err)
        kp = 1.0
        if err<0:
            pwm1.ChangeDutyCycle(val + (err*kp))
            #time.sleep(0.1)
        elif err>=0:
            pwm1.ChangeDutyCycle(val - (err*kp))
            #time.sleep(0.1)
            
    list_of_gpio.append(counter)
    list_of_gpio_2.append(counter2)
    
def left(val):
    pin = 33
    pin2 = 37
    pwm1 = gpio.PWM(pin,50)
    pwm1.start(val)
    pwm4 = gpio.PWM(pin2,50)
    pwm4.start(val)
    t = time.time()
    counter = np.uint64(0)
    counter2 = np.uint64(0) 
    button = int(0)
    button2 = int(0)
    time.sleep(0.1)
    if int (gpio.input(12)) != int(button):
        button = int(gpio.input(12))
        counter+= 1
    if int (gpio.input(7)) != int(button2):
        button2 = int(gpio.input(7))
        counter2+=1    
ser = serial.Serial('/dev/ttyUSB0',9600)

count = 0
new_x_angle = 0
while True:
    if(ser.in_waiting > 0):
        count+=1
        
        line = ser.readline()
        #print(line)
        
        
        if(count>10):
            


            time_front = 3
            time_front_2 = 7
            delay_between = 0.9
            val =  50

            forward(time_front,ser)
            time.sleep(delay_between)
            curr_x = float(ser.readline()[5:9])
            print('curr_x is : ',curr_x)
            while (abs(curr_x-new_x_angle))<=90:
                line = ser.readline()
                new_x_angle = float(line[5:9])
                print('angle diff between: ',curr_x ,'and',new_x_angle, '=',abs(curr_x-new_x_angle))
                left(val)
            time.sleep(delay_between)
            print('FIRST SIDE DONE')
            new_x_angle = 0
            forward(time_front_2,ser)
            time.sleep(delay_between)
            curr_x = float(ser.readline()[5:9])
            print('curr_x is : ',curr_x)
            while (abs(curr_x-new_x_angle))<=90:
                line = ser.readline()
                new_x_angle = float(line[5:9])
                print('angle diff between: ',curr_x ,'and',new_x_angle, '=',abs(curr_x-new_x_angle))
                left(val)
            time.sleep(delay_between)
            print('SECOND SIDE DONE')
            new_x_angle = 0
            forward(time_front,ser)
            time.sleep(delay_between)
            curr_x = float(ser.readline()[5:9])
            print('curr_x is : ',curr_x)
            while (abs(curr_x-new_x_angle))<=90:
                line = ser.readline()
                new_x_angle = float(line[5:9])
                print('angle diff between: ',curr_x ,'and',new_x_angle, '=',abs(curr_x-new_x_angle))
                left(val)
            time.sleep(delay_between)
            print('THIRD SIDE DONE')
            new_x_angle = 0
            forward(time_front_2,ser)
            time.sleep(delay_between)
            curr_x = float(ser.readline()[5:9])
            print('curr_x is : ',curr_x)
            while (abs(curr_x-new_x_angle))<=90:
                line = ser.readline()
                new_x_angle = float(line[5:9])
                print('angle diff between: ',curr_x ,'and',new_x_angle, '=',abs(curr_x-new_x_angle))
                left(val)
            time.sleep(delay_between)
            break
            print('FOURTH SIDE DONE')
print('PROCESS DONE!')
print(list_of_gpio)
print(list_of_gpio_2)

file = open('gpio_values_05_ALL_fOUR_1.txt','w')
for i in list_of_gpio:
    file.write(str(i))
    file.write('\n')
file.close()
    
file = open('gpio_values_05_ALL_fOUR_2.txt','w')
for i in list_of_gpio_2:
    file.write(str(i))
    file.write('\n')
file.close()
    
file = open('imu_x.txt','w')
for i in list_of_x:
    file.write(str(i))
    file.write('\n')
file.close()

gameover()
gpio.cleanup()




