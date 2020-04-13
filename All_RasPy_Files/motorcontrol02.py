import RPi.GPIO as gpio
import time
def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(31,gpio.OUT) #IN1
    gpio.setup(33,gpio.OUT) #IN2
    gpio.setup(35,gpio.OUT) #IN3
    gpio.setup(37,gpio.OUT) #IN4
    
def gameover():
    gpio.output(31,False)
    gpio.output(33,False)
    gpio.output(35,False)
    gpio.output(37,False)
    
def forward(tf):
    init()
    gpio.output(31,True)
    
    gpio.output(33,False)
    
    gpio.output(35,False)
    
    gpio.output(37,True)
    time.sleep(tf)
    gameover()
    gpio.cleanup()
    
def reverse(tf):
    init()
    gpio.output(31,False)
    
    gpio.output(33,True)
    
    gpio.output(35,True)
    
    gpio.output(37,False)
    time.sleep(tf)
    gameover()
    gpio.cleanup()
    
def right(tf):
    init()
    gpio.output(31,True)
    
    gpio.output(33,False)
    
    gpio.output(35,True)
    
    gpio.output(37,False)

    time.sleep(tf)
    gameover()
    gpio.cleanup()
    
def left(tf):
    init()
    
    gpio.output(31,False)
    
    gpio.output(33,True)
    gpio.output(35,False)
    
    gpio.output(37,True)
    time.sleep(tf)
    gameover()
    gpio.cleanup()
    



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

while True:
    key_press = input("Enter direction:")
    if key_press == 'p':
        break
    key_input(key_press)