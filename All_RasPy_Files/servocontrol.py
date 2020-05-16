import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.OUT)
pwm = GPIO.PWM(36,40)
pwm.start(8.3)
time.sleep(1)
i = 0
for i in range(10):
    pwm.ChangeDutyCycle(9.8) #opening of the servo
    time.sleep(1)
    pwm.ChangeDutyCycle(6.0) #closing of the servo
    time.sleep(1)
pwm.stop()
GPIO.cleanup()
