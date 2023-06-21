# Librerias para multi task
import gpio_functions as gp
import time
import multiprocessing
from multiprocessing import Process, Queue, Manager
import queue as q
import traceback

# Librerias para desencriptar mensajes can
import can
import funciones as can_lib
from my_sql import my_table_functions as sql

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


def leer_canbus(queue, obj_list):
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
            timestamp = int(float(timestamp))
            
            # Buscamos que TAG estan en el ID recibido
            
            if not id_tag in my_list_id:
                #print(f"No se encontro el tag: {id_tag}")
                continue
            
            # Caso excepcional para los ID especiales
            if id_tag in my_special_id:
                objetos = my_dictionary[id_tag]
                for obj in objetos:
                    value, tag = obj.values_to_pub(data_str)
                    if ( obj.is_new_value(value) > 0 ):
                        #print([ str(timestamp), value, tag ])
                        queue.put([str(timestamp), value, tag])
                continue
            
            # Casos en los que se filtran por frecuencias
            # obj_list -> Matriz de las classes

            posicion_i = my_list_id.index(id_tag)
            #print(f"posicion = {posicion_i}")

            # Array de classes segun TAG
            array_class = obj_list[posicion_i]
            #print("---")
            i = 0
            for _class in array_class:
                status = _class.get_flag()
                #print(f"ID : {_class.get_id()} , Status = {status}")
                if status < 1:
                    continue    
                resultado = [str(timestamp)]     #payload = [ timestamp ]
                value, tag = _class.values_to_pub(data_str)
                resultado = resultado + [value, tag]    #payload = [ timestamp - value - tag_id]
                
                #print(f"Resultado = {resultado}")
                queue.put(resultado)
                _class.set_flag(0)
                #print(f"Se envio comoo dato {_class.get_id()}")
                #print("-------------------------------")
                array_class[i] = _class
                i += 1
            obj_list[posicion_i] = array_class
                
        except Exception as e:
            print(f"Error en el proceso leer_canbus : {e}")
            traceback.print_exc()

def save_in_table(queue):
    led_state = 1
    time_prev = int(time.time())
    while True:
        try:
            resultado = queue.get( timeout = 5 )
            #print(f"Guardando: {resultado}")
            time_now = int( time.time() )
            if( time_now - time_prev ) > 2:
                time_prev = time_now
            led_state = 1 - led_state
            gp.blink(green_led,led_state)
            
            sql.insert_sql_PIF(resultado[1], resultado[2], resultado[0], session)

        except q.Empty:
            gp.on_pin(green_led)

        except Exception as e:
            print(f"Error ocurrido en save_in_table: {e}")
            pass


my_dictionary = can_lib.id_can_datos

my_list_id = list( my_dictionary.keys() )

my_special_id = can_lib.special_id

my_freq_array = []
for _id in my_list_id:
    # Obtenemos el array de freq de cada TAG
    my_freq_array.append(can_lib.lista_id[_id])
#print(my_freq_array)

table = sql(my_database_name, my_table_name)
session = table.connect_to_db()

#counter = 0
if __name__ == "__main__":

    gp.set_code_utf()
    gp.gpio_output(green_led)
    gp.on_pin(green_led)

    #pool = Pool( processes = 2 )
    
    queue = Queue()
    manager = Manager()
    shared_list = manager.list( my_dictionary.values() )

    print(" -------------------- START -------------------- ")
    #result1 = pool.apply_async(leer_canbus, args= (queue, ))
    #result2 = pool.apply_async(save_in_table, args= (queue, ))
    #result3 = pool.apply_async(change_status, args= (queue2,))

    process_1 = Process(target = leer_canbus, args = (queue, shared_list,) )
    process_2 = Process(target = save_in_table, args = (queue, ) )
    
    process_1.start()
    process_2.start()

    initial_time = int(time.time())
    try:
        while True:
            actual_time = int(time.time()) + 1
            # Despues de un tiempo, habilitamos todas las clases:
            elapse_time = actual_time - initial_time
            for pos_tag, freq_array in enumerate(my_freq_array):
                temp_array_class = shared_list[pos_tag]
                for pos_id, freq in enumerate(freq_array):
                    _class = temp_array_class[pos_id]
                    if( elapse_time % freq != 0 ):
                        continue
                    _class.set_flag(1)
                    #print(f"Se habilito {_class.get_id()}")
                    temp_array_class[pos_id] = _class
                shared_list[pos_tag] = temp_array_class
            time.sleep(1)
            
    except KeyboardInterrupt:
        # Stop the tasks when Ctrl+C is pressed
        process_1.terminate()
        process_2.terminate()
        
        process_1.join()
        process_2.join()

        print("Tasks terminated.")
