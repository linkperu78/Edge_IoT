import funciones as d
from datetime import datetime as date
import time

example_input   = "Timestamp: 1671221642.857629    ID: 18fee900    X                DLC:  8    ff ff ff ff 36 02 00 00     Channel: can0"
example_input2  = "Timestamp: 1678433670.963583    ID: 18fedf80    X                DLC:  8    84 00 19 ff ff ff ff ff     Channel: can0"
example_input3 = "Timestamp: 1671221331.467349    ID: 18fef200    X                DLC:  8    6d 00 ff ff ff ff ff ff     Channel: can0"

time_canbus = "0"
id_canbus = ""
value_canbus = 0

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

timestamp,id_tag,data_str = get_data_canbus(example_input)
print(timestamp,id_tag,data_str)

while True:
    time_init = time.time()
    print(time_init)
    if id_tag in a:
        objetos = a[id_tag]
        for obj in objetos:
            m = obj.values_to_pub(data_str)
            print(f"Resultado = {m}")
        print("sucess")
        
    time.sleep(20)

