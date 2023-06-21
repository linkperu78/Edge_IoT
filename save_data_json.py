# Librerias para multi task
import gpio_functions as gp
import time
import multiprocessing
from multiprocessing import Process, Queue
import queue as q

# Librerias para desencriptar mensajes can
import can
import funciones as can_lib
from my_sql import my_table_functions as sql

my_database_name = "dato.db"
my_table_name = "salud_table"
green_led = 10

# Abrimos el puerto can0, el programa no avanzara si no se abre
can0 = None
while can0 is None:
    try:
        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
        print("Sucessfully open CAN BUS port")
    except Exception as e:
        print(e)
        time.sleep(30)


def leer_canbus(queue):
    while True:
        try:
            # Esperamos hasta 2 segundos para obtener un nuevo mensaje por CAN BUS
            msg = can0.recv( 2 )
            #print(f"Message = {msg}")

            if msg is None:
                #print("No data reciving ...")
                time.sleep(2)
                continue
            
            # Desencriptamos el mensaje CAN recibido
            timestamp, id_tag, data_str = can_lib.get_data_canbus( str(msg) )
            objetos = []
            # Buscamos que TAG estan en el ID recibido
            
            if id_tag not in my_list_id:
                continue
            
            # Caso excepcional para los ID especiales
            if id_tag in my_special_id:
                objetos = my_dictionary[id_tag]
                for obj in objetos:
                    value, tag = obj.values_to_pub(data_str)
                    if ( obj.is_new_value(value) > 0 ):
                        print([tag, value])
                        queue.put([str(timestamp), value, tag])
                continue

            for obj in objetos:
                resultado = [str(timestamp)]     #payload = [ timestamp ]
                value, tag = obj.values_to_pub(data_str)
                resultado = resultado + [value, tag]    #payload = [ timestamp - value - tag_id]
                print(resultado)
                queue.put(resultado)

        except Exception as e:
            print(e)


def save_in_table(queue):
    led_state = 1
    gp.set_code_utf()
    gp.gpio_output(green_led)
    time_prev = int(time.time())
    while True:
        try:
            time_now = int( time.time() )
            if( time_now - time_prev ) > 2:
                time_prev = time_now
                led_state = 1- led_state
                gp.blink(led_state)

            resultado = queue.get( timeout = 5 )
            sql.insert_sql_PIF(resultado[1], resultado[2], resultado[0], session)

        except q.Empty as e:
            gp.on_pin(green_led)

        except Exception as e:
            pass


my_dictionary = can_lib.id_can_datos
my_list_id = list( my_dictionary.keys() )
my_special_id = can_lib.special_id

table = sql(my_database_name, my_table_name)
session = table.connect_to_db()

#counter = 0
if __name__ == "__main__":

    gp.set_code_utf()
    gp.gpio_output(green_led)
    gp.on_pin(green_led)

    queue = Queue()

    # Global counter
    counter = multiprocessing.Value('i', 0)
    
    print(" -------------------- START -------------------- ")
    # First Process
    read_process = Process( target = leer_canbus, args = (queue, ) )

    # Second Process
    #save_process = Process( target = save_in_table, args = (queue, ) )

    # Start processes
    read_process.start()
    #save_process.start()

    # Wait for both process to finish
    read_process.join()
    #save_process.join()

