import funciones as d
from datetime import datetime as date
import time
import can
import json


example_input   = "Timestamp: 1671221642.857629    ID: 18fee900    X                DLC:  8    ff ff ff ff 36 02 00 00     Channel: can0"


time_canbus = "0"
id_canbus = ""
value_canbus = 0

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_native')

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
        if new_temp == "DLC:":
            i += 1
            pos_data = int(temp[i])
            for j in range(pos_data):
                data_canbus_str.append(temp[j+i+1])
            break; 
        i += 1
    return [pos_time,pos_id,data_canbus_str]

a = d.id_can_datos

name_file = date.now().strftime("%m_%d_%H_%M")
print(name_file)

file_json_path = "json_data/" + name_file + ".json"

while True:
    dato = can0.recv(2.0)
    #dato = example_input
    timestamp,id_tag,data_str = get_data_canbus(dato)
    if id_tag in a:
        objetos = a[id_tag]
        for obj in objetos:
            resultado = [timestamp]
            m = obj.values_to_pub(data_str)
            resultado = resultado + m
            #print(resultado)
            json_data = {
                "F": resultado[0],
                "P": resultado[1],
                "I": resultado[2]
            }
            d.save_data(json_data,file_json_path)
    time.sleep(2.0)

