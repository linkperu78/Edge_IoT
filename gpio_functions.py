import Jetson.GPIO as GPIO


def set_code_utf():
    GPIO.setmode(GPIO.BCM)

def gpio_output(pin_number):
    GPIO.setup(pin_number, GPIO.OUT)

def on_pin(pin_number):
    GPIO.output(pin_number, GPIO.HIGH)

def off_pin(pin_number):
    GPIO.output(pin_number, GPIO.LOW)

def blink(pin_number, status):
    if status:
        GPIO.output(pin_number, GPIO.HIGH)
    else:
        GPIO.output(pin_number, GPIO.LOW)