import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)

output_pins = [4,5,6,7,8,9,10,11,12,14,15,17,18,22,23,24,25,26]
input_pins = [13,16,19,20,21,26]

for pin in output_pins :
	gpio.setup(pin, gpio.OUT)

for pin in input_pins :
	gpio.setup(pin, gpio.IN)
