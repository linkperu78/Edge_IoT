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
import header_values as const
import mySD
#from extensions import db


my_database_name = const.name_database
my_table_name = const.name_salud_no_enviados

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


def leer_canbus(queue_can, queue_time, queue_horometro):
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
                if tag == "RPM" or tag == "RPMDeseado":
                    my_horometro = [tag, value]
                    queue_horometro.put(my_horometro)
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
    engine      = SQL.create_engine(my_database_name)
    session     = SQL.create_session(engine)
    #my_model    = M.Salud_NE()

    while True:
        try:
            resultado = queue.get( timeout = 5 )
            print(f"Guardando: {resultado}")
            time_now = int( time.time() )
            
            if( time_now - time_prev ) > 1:
                time_prev = time_now
                led_state = 1 - led_state
                gp.blink(green_led,led_state)
            #print(" ----- ")
            my_model = M.Salud_NE()
            my_model.P = resultado['P']
            my_model.I = resultado['I']
            my_model.F = resultado['F']
            #print(f"SQL = {resultado}")
            #new_data = my_model(P = resultado['P'], 
                                #I = resultado['I'], 
                                #F = resultado['F'])
            session.add( my_model )
            session.commit()
            #print("done")

        except q.Empty:
            gp.on_pin(green_led)

        except Exception as e:
            print(f"Error ocurrido en save_in_table: {e}")
            pass


def horometro(queue_horometro, queue_can):
    # Obtenemos el valor almacenado en un archivo .file
    my_initial_horometro = mySD.leer_horometro_sd()
   
    # Tenemos que  esperar a que el equipo arranque:
    my_flag = 0
    while my_flag == 0:
        flag = queue_horometro.get( timeout = 10 )
        if (flag == None):
            #time.sleep(10)
            continue
        tag, value = flag
        if tag == "RPMDeseado":
            if value > 600:
                my_flag = 1
        
    # El valor en que comenzamos a leer el canbus
    my_initial_time = time.time()
    
    # Comenzamos la supervision del horometro
    while True:
        try:
            new_elapse_time = time.time() - my_initial_time
            flag = queue_horometro.get( timeout = 10 )
            if ( flag == None ):
                continue
            tag, value = flag
            if not tag == "RPM":
                continue
            if value > 800:
                queue_can.put()
                
            
        except Exception as e:
            print(f"Error en Horometro {e}")
            time.sleep(10000)



my_list_id = can_lib.get_array_tag()

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
        process_3.terminate()
        process_1.join()
        process_2.join()
        process_3.join()
        print("Tasks terminated.")
