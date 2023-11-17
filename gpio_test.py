import Jetson.GPIO as GPIO
import time

# Set the GPIO pin mode
pin1 = 10  # GPIO pin 10
pin2 = 24
GPIO.setmode(GPIO.BCM)  # Use the physical pin numbering scheme

# Set the pin as an output
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

try:
    while True:
        # Turn the LED on
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.HIGH)
        time.sleep(3)  # Sleep for 1 second

        # Turn the LED off
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)
        time.sleep(3)  # Sleep for 1 second

except KeyboardInterrupt:
    pass

# Clean up and release the GPIO pin
GPIO.cleanup()

