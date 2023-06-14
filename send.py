import os
import can
from datetime import datetime
import time
import random

can1 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
send_count = 0
timestamp = 0

id_list = { "0x0cf00300"    : {2, 2},
            "0x0cf00400"    : {3, 3}, 
            "0x0cfedf00"    : {1, 3},
            "0x0cfee400"    : {5, 1},
            "0x0cfee500"    : {1, 4},
            "0x0cfee900"    : {5, 4},
            "0x0cfeee00"    : {1, 4},
            "0x0cfeef00"    : {1, 8},
            "0x0cfef200"    : {1, 2},
            "0x0cfef500"    : {1, 1},
            "0x0cfef600"    : {2, 3},
            "0x0cfef700"    : {5, 2}
            }


def get_random_id():

    random_id = random.choice(id_list)
    return random_id

id = get_random_id()

while True:
    try:
        send_count = send_count + 1
        timestamp = datetime.now().timestamp()
        id = get_random_id()
        msg = can.Message(
            arbitration_id = id,
            data=[255,send_count,2,2,4,5,6,7],
            is_extended_id = True,
            timestamp = timestamp
        )
        can1.send(msg)
        #print("Current send frame count:", send_count)
        print(msg)
        if send_count == 254:
            send_count = 0
        time.sleep(0.04)
    except Exception as e:
        print(e)
        print(send_count)
        break

print("Finalizado")


