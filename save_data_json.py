# Librerias para multi task
import gpio_functions as gp
import time
from multiprocessing import Process, Queue
import queue as q
import traceback

# Librerias para desencriptar mensajes can
import can
import funciones as can_lib
import models as M
import my_sql as SQL


my_database_name = "dato.db"
my_table_name = "salud_table"
green_led = 10

# Abrimos el puerto can0, el programa no avanzara si no se abre
time.sleep(0.5)
can0 = None
while can0 is None:
    try:
        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
        print("Sucessfully open CAN BUS port")
    except Exception as e:
        print(e)
        time.sleep(30)


def leer_canbus(queue_can, queue_time):
    my_dict = can_lib.create_dictionary()
    init_time = int( time.time() )

    while True:
        try:
            elapse_time = int( time.time() ) + 1 - init_time
        
            if queue_time.empty():
                continue
            
            timestamp, id_tag, data_str = queue_time.get()
            array_class = my_dict[id_tag]

            # Array de classes segun TAG
            for _class in array_class:
                array_result = _class.values_to_pub(data_str, elapse_time * 10)
                if array_result == None :
                    continue
                value, tag = array_result
                #payload = [ timestamp - value - tag_id]  
                resultado = {
                    'P'     : value,
                    "I"     : tag,
                    "F"     : str(timestamp),
                    "Fecha" : timestamp
                }
                queue_can.put(resultado)
                    
        except Exception as e:
            print(f"Error en el proceso leer_canbus : {e}")
            traceback.print_exc()

def save_in_table(queue):
    led_state   = 1
    time_prev   = int(time.time())
    Model       = M.create_model_tpi(my_table_name)
    engine      = SQL.create_engine(my_database_name)
    session     = SQL.create_session(engine)

    while True:
        try:
            resultado = queue.get( timeout = 5 )
            #print(f"Guardando: {resultado}")
            time_now = int( time.time() )
            if( time_now - time_prev ) > 1:
                time_prev = time_now
                led_state = 1 - led_state
                gp.blink(green_led,led_state)
            
            #print(f"SQL = {resultado}")
            new_data = Model(P = resultado['P'], 
                             I = resultado['I'], 
                             F = resultado['F'],
                             Fecha = resultado['Fecha'])
            session.add(new_data)
            session.commit()

        except q.Empty:
            gp.on_pin(green_led)

        except Exception as e:
            print(f"Error ocurrido en save_in_table: {e}")
            pass


my_list_id = can_lib.get_array_tag()

if __name__ == "__main__":
    gp.set_code_utf()
    gp.gpio_output(green_led)
    gp.on_pin(green_led)
    
    queue_can = Queue()
    queue_time = Queue()

    print(" -------------------- START -------------------- ")
    process_1 = Process(target = leer_canbus, args = (queue_can, queue_time,) )
    process_2 = Process(target = save_in_table, args = (queue_can, ) )
    
    process_1.start()
    process_2.start()

    initial_time = int(time.time())
    try:
        while True:
            msg = can0.recv( 2 )
            #print(f"Message = {msg}")
            if msg is None:
                time.sleep(2)
                continue
            timestamp, id_tag, data_str = can_lib.get_data_canbus( str(msg) )
            if not id_tag in my_list_id:
                continue
            timestamp = int(float(timestamp))
            queue_time.put([timestamp, id_tag, data_str])
   
    except KeyboardInterrupt:
        # Stop the tasks when Ctrl+C is pressed
        process_1.terminate()
        process_2.terminate()

        process_1.join()
        process_2.join()

        print("Tasks terminated.")
