#automatically rotate the wheel for one rotation and test the encoder
import RPi.GPIO as gpio
import time
import numpy as np

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(31,gpio.OUT) #IN1
    gpio.setup(33,gpio.OUT) #IN2
    gpio.setup(35,gpio.OUT) #IN3
    gpio.setup(37,gpio.OUT) #IN4
    
    gpio.setup(12,gpio.IN,pull_up_down = gpio.PUD_UP)
def gameover():
    gpio.output(31,False)
    gpio.output(33,False)
    gpio.output(35,False)
    gpio.output(37,False)

#MAIN CODE
    
init()

counter = np.uint64(0)
button = int(0)

#initialize pwm signal to control motor

pwm = gpio.PWM(37,50)
val = 14
pwm.start(val)
time.sleep(0.1)


list_of_gpio = []
for i in range(0,100000):
    print("counter = ",counter,"GPIO state : ",gpio.input(12))
    list_of_gpio.append(gpio.input(12))
    if int (gpio.input(12)) != int(button):
    
        button = int(gpio.input(12))
        counter += 1
    if counter >= 20:
         pwm.stop()
         gameover()
         print("THANKS")
         break
file = open('gpio_values_02.txt','w')
for i in list_of_gpio:
    file.write(str(i))
    file.write('\n')
file.close()
