import os
import can
from datetime import datetime
import time
import random

can1 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
send_count = 0
timestamp = 0

def get_random_id():
    id_list = [0x0cf00300, 0x0cf00400, 0x0cfedf00,0x18fef600,0x18fef200, 0x18feef00, 0x18fee900,
        0x18fef500, 0x18fef700, 0x18feee00]
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


