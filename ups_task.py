import ups_lib as ups
import time

# When the CAT machine is shutdown, the keep alive with this counter
# a certain time equal to = (_DEFAULT_COUNT_MAX + 1) * _WINDOW_TICK seconds
# Reason: just in case the operator stop the machine accidentally
_DEFAULT_COUNT_MAX  = 100
_WINDOW_TICK        = 2

# Main program
if __name__ == '__main__':
    print("Iniciamos el supervisor de bateria")
    # From the library ups_lib.py
    ina219 = ups.INA219(addr = ups._DEFAULT_ADDRESS)
    enable_off = 0      # This start the countdown
    current = 0         # This is for storage the current current
    count_down = _DEFAULT_COUNT_MAX     # The time count remaining
    time.sleep(3)
    # This is for let the device start up all another functionarlities

    while True:
        current = ina219.getCurrent_mA()
        #print(f"Corriente actual = {current}")
        if(current < - 100) :   # Machine is powered off
            enable_off = 1
        else:                   # Machine is powered on
            enable_off = 0
            count_down = _DEFAULT_COUNT_MAX     # Restart the countdown

        # The countdown start until current will get major to zero, the device will powered off
        if(enable_off):
            print(" Apagando el equipo en {:1.0f}".format(count_down))
            # The countdown reach zero
            if(count_down < 1):
                print("Equipo apagandose a las" + str( int( time.time() ) ))
                ups.shut_down()
            count_down -= 1
        time.sleep(2)
