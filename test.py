import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(25, GPIO.OUT) # LED pin set as output
GPIO.output(25, GPIO.HIGH)
