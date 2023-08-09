import can
import time
import funciones as can_lib

time.sleep(0.5)
can0 = None
while can0 is None:
    try:
        can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
        print("Sucessfully open CAN BUS port")
    except Exception as e:
        print(e)
        time.sleep(30)

try:
    while True:
        msg = can0.recv( 2 )
        print(f"Message = {msg}")
        if msg is None:
            time.sleep(2)
            continue
        timestamp, id_tag, data_str = can_lib.get_data_canbus( str(msg) )
            #if not id_tag in my_list_id:
                #continue
        timestamp = int(float(timestamp))
            #queue_time.put([timestamp, id_tag, data_str])
    
except Exception as e:
   print(f"Error = {e}")
    
except KeyboardInterrupt:
    # Stop the tasks when Ctrl+C is pressed
    print("Tasks terminated.")
