import ups
import time
import gpio_functions as g

led_pin = 10

can_task = "can"
server_task = "server"

can_status = 1
server_status = 1

if __name__ == '__main__':
    #print("Iniciamos el supervisor de bateria")
    
    # Create an ADS1115 ADC (16-bit) instance.
    ina219 = ups.INA219(addr = ups._DEFAULT_ADDRESS)
    
    #g.set_code_utf()
    #g.gpio_output(led_pin)
    #g.on_pin(led_pin)
    
    enable_off = 0
    current = 0
    
    count_down = ups._DEFAULT_COUNT_MAX
    time.sleep(3)
    
    while True:
        #bus_voltage = ina219.getBusVoltage_V()             # voltage on V- (load side)
        current = ina219.getCurrent_mA()                   # current in mA
        if(current < - 100) :
            enable_off = 1
        else:
            enable_off = 0
            count_down = ups._DEFAULT_COUNT_MAX

        if(enable_off):
            #print(" Apagando el equipo en {:1.0f}".format(count_down))
            if(count_down < 1):
                #save_data()
                #if can_status > 0:
                    #ups.end_service(can_task)
                    #can_status = 0
                #if server_status > 0:
                    #ups.end_service(server_task)
                    #server_status = 0
                ups.shut_down()
            count_down -= 1
        time.sleep(2)
