from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Salud as Data

import time
import multiprocessing
from multiprocessing import Process, Queue
import queue as q

import funciones as d
import json
import can
import generate_data as g
import gpio_functions as gp

time_canbus = "0"
id_canbus = ""
value_canbus = 0
database_name = "dato.db"

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


# return: timestamp , tag, data_byte
def get_data_canbus(msg_canbus):
    data_canbus_str = []
    i, pos_time, pos_id, pos_data = 0,"","",0
    temp = msg_canbus.split()
    len_temp = len(temp)

    while i < len_temp:
        new_temp = temp[i]
        if new_temp == "Timestamp:":
            i += 1
            pos_time = temp[i]
            continue
        if new_temp == "ID:":
            i += 1
            pos_id = temp[i][2:6]
            continue
        if new_temp == "DL:":
            i += 1
            pos_data = int(temp[i])
            for j in range(pos_data):
                data_canbus_str.append(temp[j+i+1])
            break; 
        i += 1
    
    return [pos_time,pos_id,data_canbus_str]


# Create connection database
def connect_to_db(db_uri):
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    return Session()


# Save data in table 
def insert_data(P_value, I_value, F_value, session):
    new_data = Data(P=P_value, I=I_value, F=F_value)
    session.add(new_data)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print("Error occurred:", e)


def leer_canbus(queue):
    while True:
        try:
            msg = can0.recv( 2 )
            #print(f"Message = {msg}")
            if msg is None:
                #print("No data reciving ...")
                time.sleep(2)
                continue

            timestamp, id_tag, data_str = get_data_canbus( str(msg) )
            new_timestamp = float(timestamp)
            new_timestamp = int(new_timestamp)
            message_queue = [new_timestamp, id_tag, data_str]
            queue.put(message_queue)

        except Exception as e:
            print(e)


def save_in_table(queue):
    led_status = 1
    while True:
        #my_time = time.time()
        try:
            timestamp, id_tag, data_byte = queue.get( timeout = 2 )
            objetos = []
            if id_tag in a:
                objetos = base_data[id_tag]
                led_status = 1 - led_status
                gp.blink(green_led, led_status)

            for obj in objetos:
                resultado = [str(timestamp)]
                m = obj.values_to_pub(data_byte)
                resultado = resultado + m
                insert_data(resultado[1], resultado[2], resultado[0], session)
            
            #my_time = round( (time.time() - my_time) * 1000 , 2)
            #print(f"{my_time} ms")
        except q.Empty as e:
            gp.on_pin(green_led)

        except Exception as e:
            pass
            #print(e)
            #print(m)
        #time.sleep(0.1)

 
# Creamos la clase
base_data = d.id_can_datos

# Extraemos las llaves existentes
a = list(base_data.keys())

time_actual = time.time()

# Database URI
db_uri = 'sqlite:///instance/' + database_name

# Creating a new session
session = connect_to_db(db_uri)


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
    save_process = Process( target = save_in_table, args = (queue, ) )

    # Start processes
    read_process.start()
    save_process.start()

    # Wait for both process to finish
    read_process.join()
    save_process.join()






'''
while True:
    msg = str(can0.recv(10))
    print(msg)

    timestamp,id_tag,data_str = get_data_canbus(msg)

    objetos = []
    if id_tag in a:
        objetos = a[id_tag]

    for obj in objetos:
        resultado = [str(timestamp)]
        m = obj.values_to_pub(data_str)
        
        print("Resultado = " + str(m))
        resultado = resultado + m
        
        insert_data(resultado[1], resultado[2], resultado[0], session)
        

    print("")
    #time.sleep(0.0001)
'''
