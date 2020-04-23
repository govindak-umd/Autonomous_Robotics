#manually rotate the wheels and test the encoder
import RPi.GPIO as gpio
import time
import numpy as np


def init():
    gpio.setmode(gpio.BOARD)
    
    gpio.setup(12,gpio.IN,pull_up_down = gpio.PUD_UP)

def gameover():
    gpio.cleanup()


init()
counter = np.uint64(0)
button = int(0)

while True:
    if int(gpio.input(12))!=int(button):
        button = int(gpio.input(12))
        counter+=1
        print(counter)
    if counter>=20:
        gameover()
        print("exit")
        break