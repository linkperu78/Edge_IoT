from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Salud as Data
from datetime import datetime as date

import time
import funciones as d
import json
import can
import generate_data as g


time_canbus = "0"
id_canbus = ""
value_canbus = 0

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
database_name = "dato.db"


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

def connect_to_db(db_uri):
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    return Session()

def insert_data(P_value, I_value, F_value, session):
    new_data = Data(P=P_value, I=I_value, F=F_value)
    session.add(new_data)
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print("Error occurred:", e)
        return None
    #return new_data

a = d.id_can_datos

name_file = date.now().strftime("%m_%d_%H_%M")

print(name_file)
file_json_path = "json_data/" + name_file + ".txt"
time_actual = time.time()

# Database URI
db_uri = 'sqlite:///instance/' + database_name

# Creating a new session
session = connect_to_db(db_uri)


while True:
    #actual_timestamp = time.time()
    #time_elapse = int(actual_timestamp - time_actual)
    #print(f" {actual_timestamp} ")    
    #if(time_elapse == 0):
    #    time.sleep(1)
    #    continue
    #print(" ----- ")
    #print(f"- Tiempo transcurrido: {time_elapse}")
    #print(" ----- ")
    
    msg = str(can0.recv(10))
    print(msg)
    #d.save_data(msg,file_json_path)

    timestamp,id_tag,data_str = get_data_canbus(msg)
    #timestamp = actual_timestamp
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
