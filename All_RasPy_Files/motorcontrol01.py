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
    gpio.output(31,False)
    
    gpio.output(33,True)
    
    gpio.output(35,True)
    
    gpio.output(37,False)
    time.sleep(tf)
    gameover()
    gpio.cleanup()
    
def reverse(tf):
    init()
    gpio.output(31,True)
    
    gpio.output(33,False)
    
    gpio.output(35,False)
    
    gpio.output(37,True)
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
    
def right(tf):
    init()
    
    gpio.output(31,True)
    
    gpio.output(33,False)
    gpio.output(35,True)
    
    gpio.output(37,False)
    time.sleep(tf)
    gameover()
    gpio.cleanup()
    

forward(2)
time.sleep(3)
reverse(2)
time.sleep(3)
left(2)
time.sleep(3)
right(2)