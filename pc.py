import class_can as my_class
import time
import can

dias_time = 24 * 3600 
can_port = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

# Creamos un diccionario de los TAGS del CANBUS
canbus = my_class.valores_canbus()

# Extraemos los TAGS registrados y sus frecuencias relacionadas
array_frecuencias = []
array_tags = []
for key in canbus.dictionary.keys():
    array_tags.append(key)
    array_frecuencias.append(canbus.dictionary[key]['freq'])

my_actual_time = int( time.time() )
time_max_simulation = 2 * dias_time + my_actual_time

time_multiplier = 10
my_counter = 1
while my_actual_time < time_max_simulation:
    try:
        for nu, freq in enumerate(array_frecuencias):
            if ( my_counter % freq == 0):
                tag = array_tags[nu]
                byte_can = canbus.actualizar_valor(tag)
                #print(f"{tag} - {canbus.actualizar_valor(tag)} - {i}")
                
                msg = can.Message(
                arbitration_id = int(tag,16),
                data=byte_can,
                is_extended_id = True,
                timestamp = my_actual_time
                )
                #print(msg)
                can_port.send(msg)
        my_counter += 1
        time.sleep( 1 / time_multiplier )
        my_actual_time = int( time.time() )
        #print("---")
    except Exception as e:
        print(f"Error en {tag} = {e}")
        time.sleep(10)

print("Finalizado")