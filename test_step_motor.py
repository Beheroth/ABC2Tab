from time import sleep
import RPi.GPIO as gpio

pin_dir = 20
pin_val = 21
pin_sleep = 16

gpio.setmode(gpio.BCM)
gpio.setup(pin_dir, gpio.OUT)
gpio.setup(pin_val, gpio.OUT)
gpio.setup(pin_sleep, gpio.OUT)

gpio.output(pin_dir, gpio.HIGH)
gpio.output(pin_sleep, gpio.HIGH)

imp = 0
print("start")
while imp < 1000:
	gpio.output(pin_val, gpio.HIGH)
	sleep(0.0008)
	gpio.output(pin_val, gpio.LOW)
	sleep(0.0008)
	imp+=1
print("end")

gpio.output(pin_dir, gpio.LOW)
gpio.output(pin_sleep, gpio.LOW)
gpio.output(pin_val, gpio.LOW)
