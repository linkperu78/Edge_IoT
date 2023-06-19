import gpio_functions as gpio
import time

pin = 10
gpio.set_code_utf()

gpio.gpio_output(pin)

while True:
    gpio.on_pin(10)
    time.sleep(1)
    gpio.off_pin(10)
    time.sleep(1)


