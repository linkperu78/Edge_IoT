import time
import random

data_fedf = "Timestamp: 1671221805.427533    ID: 0cfedf00    X                DLC:  8    84 00 19 ff ff ff ff ff     Channel: can0"
data_f003 = "Timestamp: 1671221755.885560    ID: 0cf00300    X                DLC:  8    ff 00 00 ff ff ff ff ff     Channel: can0"
data_fef6 = "Timestamp: 1671221777.751517    ID: 18fef600    X                DLC:  8    ff 00 4a 32 ff ff ff ff     Channel: can0"
data_feef = "Timestamp: 1671221775.947908    ID: 18feef00    X                DLC:  8    42 ff ff ff ff ff ff fa     Channel: can0"
data_fee9 = "Timestamp: 1671221642.857629    ID: 18fee900    X                DLC:  8    ff ff ff ff 36 02 00 00     Channel: can0"

data_rate = {
    "1" : {
        "data" : data_fedf,
        "rate" : 1  
    },
    "2" : {
        "data" : data_f003,
        "rate" : 5
    },
    "3":{
        "data" : data_fef6,
        "rate" : 8
    },
    "4" : {
        "data" : data_feef,
        "rate" : 10
    },
    "5" : {
        "data" : data_fee9,
        "rate" : 5
    }
}

def generar_data(time_elapse):
    mensaje = []
    for key in data_rate.keys():
        if time_elapse > data_rate[key]["rate"]:
            mensaje.append(data_rate[key]["data"])
    return mensaje

def print_enter(mensajes):
    for msg in mensajes:
        print(msg)
