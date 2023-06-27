# Librerias para multi task
import gpio_functions as gp
import time
from multiprocessing import Process, Queue
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

while True:
    msg = can0.recv( 2 )
    print(msg)
