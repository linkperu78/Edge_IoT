# Librerias para multi task
import gpio_functions as gp
import time
from multiprocessing import Process, Queue
import queue as q
import traceback

# Librerias para desencriptar mensajes can
import can
import canbus_funciones as can_lib
import models as M
import sql_library as SQL
import json_reader

# Importamos los datos del json
green_led = json_reader.get_json_from_file("machine_values.json")["Led"]

# SQL data
sql_data = json_reader.get_json_from_file("sql_names.json")
database_name   = sql_data["name"]
salud_sql       = sql_data["table_salud"]

acelerador      = 1

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


#
# Process to decode canbus data 
#
def leer_canbus(queue_can, queue_time, queue_horometro):
    my_dict = can_lib.create_dictionary()
    init_time = int( time.time() )

    while True:
        try:
            # Obtenemos el tiempo que ha pasado para filtrar por frecuencias
            # + 1 para evitar que todos se actualicen
            elapse_time = int( time.time() ) + 1 - init_time
            elapse_time = elapse_time * acelerador

            if queue_time.empty():
                continue

            timestamp, id_tag, data_str = queue_time.get()
            array_class = my_dict[id_tag]

            # Array de classes segun TAG
            for _class in array_class:
                _enable, array_result = _class.values_to_pub(data_str, elapse_time)
                value, tag = array_result
                
                # Pasamos el valor de RPMDeseado a task horometro
                if ( tag == "RPMDeseado" ):
                    queue_horometro.put(value)

                # _enable = 1 : Se habilito la publicacion por filtro
                if _enable == 0 :
                    continue
                
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


#
# Process to save data in SQL Database#
#
def save_in_table(queue):
    led_state   = 1
    time_prev   = int(time.time())
    sql_host = SQL.sql_host()
    sql_host.set_name_db(database_name)
    Salud_Model = M.create_model_salud_tpi(salud_sql)
    while True:
        try:
            resultado = queue.get( timeout = 5 )
            print(f"Guardando: {resultado}")
            time_now = int( time.time() )
            if( time_now - time_prev ) > 1:
                time_prev = time_now
                led_state = 1 - led_state
                gp.blink(green_led,led_state)

            sql_host.insert_data(Salud_Model, resultado)

        except q.Empty:
            gp.on_pin(green_led)
        except Exception as e:
            print(f"Error ocurrido en save_in_table: {e}")
            pass


#
# Process to run or stop the horometer parameter
#
def horometro(queue_horometro, queue_can):
    # Obtenemos el valor almacenado en un archivo .file
    horometro_value = json_reader.get_json_from_file("horometer.json")

    # Comenzamos la supervision del horometro
    prev_horometro_time = time.time()
    prev_save_file_time = prev_horometro_time
    actual_time = 0
    status_horometro = 0
    freq_muestreo = 1

    while True:
        try:
            if queue_horometro.empty():
                time.sleep(0.1)
                continue
            value_rpm = queue_horometro.get()
            actual_time = time.time()

            # Aseguramos que haya pasado 1 segundo
            elapse_time = actual_time - prev_horometro_time
            elapse_time = elapse_time * acelerador

            if elapse_time < freq_muestreo :
                continue
            #print(f"Horometer: checking speed")
            prev_horometro_time = time.time()
            if (value_rpm < 795):
                status_horometro = 0
            else:
                status_horometro = 1
            #print(f"Horometer: {status_horometro}")
            my_time = int(elapse_time)
            horometro_value["horometro"]    += my_time
            horometro_value["ralenti"]      += my_time * status_horometro
            print(horometro_value)
            # Aseguramos que hayan pasado 60 segundos
            elapse_time = actual_time - prev_save_file_time
            elapse_time = elapse_time * acelerador  
            if elapse_time < 60 :
                continue
            prev_save_file_time = prev_horometro_time
            timestamp_horometro = int( actual_time )
            #print(f"Horometer: Updating in json file")
            json_reader.save_in_json_file("horometer.json",horometro_value)
            resultado = {
                'P'     : horometro_value["ralenti"],
                "I"     : "Ralenti",
                "F"     : str(timestamp_horometro),
                "Fecha" : timestamp_horometro
            }
            queue_can.put(resultado) 
            resultado = {
                'P'     : horometro_value["horometro"],
                "I"     : "Horometro",
                "F"     : str(timestamp_horometro),
                "Fecha" : timestamp_horometro
            }
            queue_can.put(resultado)

        except Exception as e:
            print(f"Error en Horometro {e}")
            time.sleep(10000)



my_list_id = can_lib.estructura_can.canbus_tags_list

# Main Program
if __name__ == "__main__":
    gp.set_code_utf()
    gp.gpio_output(green_led)
    gp.on_pin(green_led)
    
    queue_can = Queue()
    queue_time = Queue()
    queue_horometro = Queue()

    print(" -------------------- START -------------------- ")
    process_1 = Process(target = leer_canbus, args = (queue_can, queue_time, queue_horometro,) )
    process_2 = Process(target = save_in_table, args = (queue_can, ) )
    process_3 = Process(target = horometro, args = (queue_horometro, queue_can, ) )

    process_1.start()
    process_2.start()
    process_3.start()

    initial_time = int(time.time())
    canbus_list_filter = can_lib.estructura_can.canbus_tags_list
    try:
        while True:
            msg = can0.recv( 2 )
            if msg is None:
                time.sleep(1)
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
        process_3.terminate()
        process_1.join()
        process_2.join()
        process_3.join()
        print("Tasks terminated.")
