#Autor: Gustavo Jordi Juarez Trujillo

"""
check (bool) – By default, the constructor of this class does not strictly check the input. Thus, the caller must prevent the creation of invalid messages or set this parameter to True, to raise an Error on invalid inputs. Possible problems include the dlc field not matching the length of data or creating a message with both is_remote_frame and is_error_frame set to True.
timestamp (float) –
arbitration_id (int) –
is_extended_id (bool) –
is_remote_frame (bool) –
is_error_frame (bool) –
channel (Optional[Union[int, str]]) –
dlc (Optional[int]) –
data (Optional[Union[bytes, bytearray, int, Iterable[int]]]) –
is_fd (bool) –
is_rx (bool) –
bitrate_switch (bool) –
error_state_indicator (bool) –
"""
# CON INPUT CAN BUS, OUTPUT MQTT
# Este se usará para alimentar la base de datos del node-red, debe ejecutarse automáticamente

import funciones as d
import time

import time
import json
import can
import datetime

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_native')


def subir(dic, ID, calculo):
    [data1, valor1, etiqueta1, unidad1] = calculo
    if not ID in dic.keys():
        dic[ID] = []
    dt = datetime.datetime.now()
    fecha = datetime.datetime.timestamp(dt)
    fecha = int(fecha)
    dic[ID].append([valor1, etiqueta1, unidad1, fecha])
    return dic

def subir_reducido(dic, ID, calculo):
    [data1, valor1, etiqueta1, unidad1] = calculo
    # Tiempo de timestamp 
    dt = datetime.datetime.now()
    fecha = datetime.datetime.timestamp(dt)
    fecha = str(int(fecha))
    if not ID in dic.keys():
        dic[ID] = []
    dic[ID].append([ str(valor1), fecha])
    return dic

def mostrar(calculo, j):
    idd = " "*15
    [ valor1, etiqueta1, unidad1, fecha] = calculo
    idd = j + idd
    print(idd[0:15] +": "+str(etiqueta1)+" "+str(valor1)+ " "+ str(unidad1)  )


#Inicializar variables

while True:
    dato = can0.recv(2.0)
    if dato is None:
        print('No message was received')
        time.sleep(0.01)
        continue
    print(dato)


