#automatically rotate the wheel for one rotation and test the encoder
import RPi.GPIO as gpio
import time
import numpy as np
import serial
ser = serial.Serial('/dev/ttyUSB0',9600)

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(31,gpio.OUT) #IN1
    gpio.setup(33,gpio.OUT) #IN2
    gpio.setup(35,gpio.OUT) #IN3
    gpio.setup(37,gpio.OUT) #IN4
    #right back wheel encoder
    gpio.setup(12,gpio.IN,pull_up_down = gpio.PUD_UP)
    #left front wheel encoder
    gpio.setup(7,gpio.IN,pull_up_down = gpio.PUD_UP)
def gameover():
    gpio.output(31,False)
    gpio.output(33,False)
    gpio.output(35,False)
    gpio.output(37,False)

#MAIN CODE
    
init()

counter = np.uint64(0)
counter2 = np.uint64(0) 
button = int(0)
button2 = int(0)

#initialize pwm signal to control motor

pwm1 = gpio.PWM(37,50)
pwm4 = gpio.PWM(31,50)
val = 20
pwm1.start(val)

pwm4.start(val)
time.sleep(0.1)

list_of_gpio = []
list_of_gpio_2 = []
for i in range(0,200000):

    #print("counter = ",counter,"GPIO state ( 12 ): ",gpio.input(12))
    #print("counter = ",counter,"GPIO state ( 7 ): ",gpio.input(7))
    list_of_gpio.append(gpio.input(12))
    list_of_gpio_2.append(gpio.input(7))
    if int (gpio.input(12)) != int(button):
        button = int(gpio.input(12))
        
    if int (gpio.input(7)) != int(button2):
        button2 = int(gpio.input(7))
        counter2+=1
    #1 rpm  = 2   * 3.14 * 0.0325 m
    #1 rpm  = 20 ticks
    #x rpm  = 20 *(0.914   * ((6.28) * 0.0325)) m
        #= 177 ticks
    print('wheel has rotated ',counter,'times')
    if counter >= 90:
         pwm1.stop()
         pwm4.stop()
         gameover()
         print("test complete.")
         gpio.cleanup()
         break

file = open('gpio_values_05_1.txt','w')
for i in list_of_gpio:
    file.write(str(i))
    file.write('\n')
file.close()


file = open('gpio_values_05_2.txt','w')
for i in list_of_gpio_2:
    file.write(str(i))
    file.write('\n')
file.close()


