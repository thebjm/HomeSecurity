#!/usr/bin/python3

import subprocess
import os
import time
import RPi.GPIO as GPIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mail = os.path.join(BASE_DIR, 'mail.py')
target = os.path.join(BASE_DIR, 'recognize_video.py')

print(target)

GPIO.setmode(GPIO.BCM)

servo = 4
pir_sensor = 17
piezo = 27
pushbtn = 20

GPIO.setup(servo,GPIO.OUT)
pwm = GPIO.PWM(servo,50)
#pwm.start(7.5)
pwm.start(13)
pwm.ChangeDutyCycle(1)
time.sleep(1)
pwm.stop()
print('[INFO] locking Door..')

GPIO.setup(piezo,GPIO.OUT)
GPIO.setup(pir_sensor, GPIO.IN)
GPIO.setup(pushbtn, GPIO.IN, pull_up_down = GPIO.PUD_UP)
current_state = 0


def siren():
    current_state = GPIO.input(pir_sensor)
    if current_state == 1:
        print("GPIO pin %s is %s" % (pir_sensor, current_state))
        GPIO.output(piezo,True)
        time.sleep(0.5)
        GPIO.output(piezo,False)
        time.sleep(.5)
        subprocess.call('python3 ' +mail, shell = True )
        current_state == 0
                 
    else:
        print("GPIO pin %s is %s" % (pir_sensor, current_state))
        GPIO.output(piezo,True)
        time.sleep(0.5)

try:
    GPIO.output(piezo,True)
    time.sleep(2)
   
    
    while True:
        siren()
        
        input_state = GPIO.input(20)
        if input_state == False:
            GPIO.output(piezo,True)
            time.sleep(0.5)
            print('button Pressed')
            
            break
       
        
            
except KeyboardInterrupt:
    GPIO.output(piezo,True)
    time.sleep(0.5)
    pass


subprocess.call('python3 ' +target, shell = True )
