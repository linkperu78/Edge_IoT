## Librerias para comunicacion RS 485
import  rs485_lib as rs485
import  serial

## Librerias para multi tarea
from    multiprocessing import Process, Queue
import  queue
import  traceback
from    time import time, sleep

## Librerias para SQL
import models as MODEL
import sql_library as SQL

## ONLY change for testing, in production must be "1"
MULTIPLIER_TIME = 3


## Upload the data for SQL database
sql_dictionary      = rs485.get_json_from_file("sql_names.json")
database_name       = sql_dictionary["name"]


## Path for R1300 CAT Data Link parameters ( scale, offset, ID register, etc)
## Upload the data for read CDL data
json_file           = "parameters.json"
rs485_class         = rs485.cdl_rs485(json_file)
array_keys_id       = rs485_class.get_array_id()
dictionary_for_eval = rs485_class.get_basic_dictionary()

## Tarea para hacer blink en el led
def led_green_blink(cola_led_verde):
    pass

## Funcion para tarea de guardar datos en la base de datos SQL
def task_update_database(cola_sql, class_cdl):
    salud_table_model = MODEL.salud_model
    time_prev   = int( time() )
    sql_host    = SQL.sql_host()
    sql_host.set_name_db(database_name)

    r1300g_dictionary = class_cdl.r1300g_dictionary

    while True:
        try:
            if cola_sql.empty():
                sleep(0.1)
                continue
            array_tag, offset, rs485_data = cola_sql.get()

            time_actual = int(time())
            for key in array_tag:
                value_in_hex = []
                decimal_value = 0
                array_pos_byte = r1300g_dictionary[key]["Registro"]
                
                for pos_byte in array_pos_byte:
                    _pos = (pos_byte - offset) * 2
                    value_in_hex += rs485_data[ _pos:_pos + 2 ]
                value_in_hex = value_in_hex[::-1]
                hex_string = ''.join(format( x , '02x' ) for x in value_in_hex)
                decimal_value = int(hex_string, 16)
                
                ## Evaluamos el valor obtenido
                max_possible_value  = r1300g_dictionary[key]["max"]
                min_possible_value  = r1300g_dictionary[key]["min"]
                scale_value         = r1300g_dictionary[key]["scale"]
                offset_value        = r1300g_dictionary[key]["offset"]
                value_to_save       = decimal_value * scale_value + offset_value
                
                ## Valor fuera de rango: Ignoramos el valor, no lo almacenamos
                if( value_to_save > max_possible_value or 
                    value_to_save < min_possible_value):
                    continue

                ## Guardamos el valor decimal en la base de datos:
                json_for_save = {
                    "P" : value_to_save,
                    "F" : str(time_actual),
                    "I" : key,
                }
                sql_host.insert_data(salud_table_model, json_for_save)

        except Exception as e:
            print(f"Error ocurrido en save_in_table: {e}")


if __name__ == "__main__":
    
    queue_sql   = Queue()
    queu_led    = Queue()
    process_1   = Process(target = task_update_database, args = (queue_sql, rs485_class) )
    #process_2   = Process(target = led_green_blink, args = (queu_led, ) )
    process_1.start()
    #process_2.start()

    ## Variables de tiempo para frecuencia
    actual_time         = int(time()) - 1
    prev_elapse_time    = 0
    init_time           = actual_time

    try:
        print("Lector de CDL Data ha iniciado")
        ## Configure the serial port
        port_rs485 = serial.Serial(
            port='/dev/ttyUSB0',    ## For Jetson Nano
            #port = 'COM6',          ## For Windows
            baudrate=9600,
            ## Default values for Serial         
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        while True:
            actual_time = int(time())
            elapse_time = int ( (actual_time - init_time) * MULTIPLIER_TIME )
            if (elapse_time == prev_elapse_time):
                sleep(0.5)
                continue
            
            array_reg_request_rs485 = []
            array_id_request_rs485 = []

            ## Evaluamos si ya ha pasado el tiempo necesario para solicitar registros
            for parameter_id in array_keys_id:
                freq_id = dictionary_for_eval[parameter_id]['freq']
                ## Si el tiempo transcurrido es multiplo de la frecuencia establecida
                ## Generamos el array a solicitar
                if( elapse_time % freq_id == 0 ):
                    reg_get     = dictionary_for_eval[parameter_id]["reg"]
                    array_id_request_rs485.append(parameter_id)
                    array_reg_request_rs485 += reg_get

            if (len(array_reg_request_rs485) > 0):
                ## Enviamos la consulta hacia el equipo CAInstruments
                ## por el UART RS485
                min_value = min(array_reg_request_rs485)
                query_byte = rs485_class.rs485_request(1, 
                                                       min_value, 
                                                       max(array_reg_request_rs485))
                port_rs485.write(bytearray(query_byte))
                print(f"Tag a consultar = {array_id_request_rs485}\nArray_registros = {array_reg_request_rs485}\nRequest = '{query_byte}\n")
                ## Obtenemos la respuesta del equipo
                data = port_rs485.read(100)
                if(data):
                    cdl_response = data.hex()
                    data_to_send_sql = [array_id_request_rs485, min_value, data[3:-2]]
                    queue_sql.put(data_to_send_sql) 

            prev_elapse_time = elapse_time
            sleep(0.1)
   
    except KeyboardInterrupt:
        ## Detener todas las tareas cuando se cancela el script
        ## con "CTRL + C"
        process_1.terminate()
        #process_2.terminate()
        process_1.join()
        #process_2.join()
        print("Tareas finalizadas")