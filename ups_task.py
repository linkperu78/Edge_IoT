import ups
import time
import gpio_functions as g

led_pin = 10

can_task = "can"
server_task = "server"

can_status = 1
server_status = 1

if __name__ == '__main__':
    print("Iniciamos el supervisor de bateria")
    ina219 = ups.INA219(addr = ups._DEFAULT_ADDRESS)
    enable_off = 0
    current = 0
    
    count_down = ups._DEFAULT_COUNT_MAX
    time.sleep(3)
    
    while True:
        current = ina219.getCurrent_mA()
        if(current < - 100) :
            enable_off = 1
        else:
            enable_off = 0
            count_down = ups._DEFAULT_COUNT_MAX

        if(enable_off):
            print(" Apagando el equipo en {:1.0f}".format(count_down))
            if(count_down < 1):
                print(f"Equipo apagandose a las { int( time.time() ) }")
                ups.shut_down()
            count_down -= 1
        time.sleep(2)
