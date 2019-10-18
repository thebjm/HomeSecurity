import RPi.GPIO as GPIO
import time
import subprocess
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

target = os.path.join(BASE_DIR, 'recognize_video.py')

GPIO.setmode(GPIO.BCM)
servo = 4
pir_sensor = 17
piezo = 27
pushbtn2 = 21

def doorLock():
	GPIO.setup(servo,GPIO.OUT)
	pwm = GPIO.PWM(servo,50)
	#pwm.start(7.5)
	pwm.start(13)
	pwm.ChangeDutyCycle(1)
	time.sleep(1)
	pwm.stop()
	print('[INFO] locking Door..')


GPIO.setup(pushbtn2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
	input_state = GPIO.input(21)
	
	if input_state == False:
		print('button Pressed')
		doorLock()
		subprocess.call('python3 ' +target, shell = True )
		
		time.sleep(0.2)
		
