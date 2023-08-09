import ups
import time

_DEFAULT_COUNT_MAX = 4

if __name__ == '__main__':
    print("Iniciamos el supervisor de bateria")
    ina219 = ups.INA219(addr = ups._DEFAULT_ADDRESS)
    enable_off = 0
    current = 0
    
    count_down = _DEFAULT_COUNT_MAX
    time.sleep(3)
    
    while True:
        current = ina219.getCurrent_mA()
        #print(f"Corriente actual = {current}")
        if(current < - 100) :
            enable_off = 1
        else:
            enable_off = 0
            count_down = _DEFAULT_COUNT_MAX

        if(enable_off):
            print(" Apagando el equipo en {:1.0f}".format(count_down))
            if(count_down < 1):
                print("Equipo apagandose a las" + str( int( time.time() ) ))
                ups.shut_down()
            count_down -= 1
        time.sleep(2)
