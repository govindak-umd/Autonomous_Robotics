#automatically rotate the wheel for one rotation and test the encoder
import RPi.GPIO as gpio
import time
import numpy as np

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


counter = np.uint64(0)
counter2 = np.uint64(0) 
button = int(0)
button2 = int(0)

#initialize pwm signal to control motor
angle = 90 #USER DEFINED ANGLE
ticks = (angle/90)*4
print('ticks to turn by an angle',angle,' is : ',ticks)
pin = 31
pin2 = 37
pwm1 = gpio.PWM(pin,50)
pwm4 = gpio.PWM(pin2,50)
time.sleep(2)
val = 30
list_of_gpio = []
list_of_gpio_2 = []
for i in range(0,200000):
    

    
    pwm1.start(val)

    pwm4.start(val)
    time.sleep(0.1)


    #print("counter = ",counter,"GPIO state ( 12 ): ",gpio.input(12))
    #print("counter = ",counter,"GPIO state ( 7 ): ",gpio.input(7))
    list_of_gpio.append(gpio.input(12))
    list_of_gpio_2.append(gpio.input(7))
    if int (gpio.input(12)) != int(button):
        button = int(gpio.input(12))
        counter+= 1
    if int (gpio.input(7)) != int(button2):
        button2 = int(gpio.input(7))
        counter2+=1
    #1 rpm  = 2   * 3.14 * 0.0325 m
    #1 rpm  = 20 ticks
    #x rpm  = 20 *(0.914   * ((6.28) * 0.0325)) m
        #= 177 ticks
    counter_avg = (counter+counter2)/2
    print('wheel has rotated ',counter_avg,'times')
    if counter_avg == 50 or counter_avg ==50 + 0.5:
         pwm1.stop()
         pwm4.stop()
         gameover()
         time.sleep(2)
         init()
         time.sleep(2)
         val = 80
         pwm1 = gpio.PWM(31,50)
         pwm4 = gpio.PWM(35,50)
         print("RIGHT NOW")
         #gpio.cleanup()
         
    elif counter_avg == 50 + ticks or counter_avg ==50+ticks+0.5:
    
         pwm1.stop()
         pwm4.stop()
         gameover()
         time.sleep(1)
         init()
         val = 80
         pwm1 = gpio.PWM(33,50)
         pwm4 = gpio.PWM(37,50)
         print("LEFT NOW")
         
    elif counter_avg == 50 + ticks + ticks or counter_avg == 50 + ticks + ticks + 0.5:
         pwm1.stop()
         pwm4.stop()
         gameover()
         time.sleep(2)
         init()
         time.sleep(2)
         val = 26
         pwm1 = gpio.PWM(33,50)
         pwm4 = gpio.PWM(35,50)
         print("REVERSE NOW")
         
    elif counter_avg == 50 + ticks + ticks + 50 or counter_avg == 50 + ticks + ticks + 50+0.5:
         pwm1.stop()
         pwm4.stop()
         gameover()
         print("THANKS")
         gpio.cleanup()
         break

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



