import class_can as my_class
import time
import can

#can_port = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
canbus = my_class.valores_canbus()
array_frecuencias = []
array_tags = []

for key in canbus.dictionary.keys():
    array_tags.append(key)
    array_frecuencias.append(canbus.dictionary[key]['freq'])

i = 1
n_muestras = 2_592_000
my_actual_time = int(time.time())


while i < n_muestras:
    try:
        for nu,freq in enumerate(array_frecuencias):
            if ( i % freq == 0):
                tag = array_tags[nu]
                byte_can = canbus.actualizar_valor(tag)
                #print(f"{tag} - {canbus.actualizar_valor(tag)} - {i}")
                
                msg = can.Message(
                arbitration_id = int(tag,16),
                data=byte_can,
                is_extended_id = True,
                timestamp = my_actual_time
                )
                #can_port.send(msg)

        my_actual_time += 1
        i += 1
        time.sleep(0.0002)
    except Exception as e:
        print(e)
    
    if(i % 28_800 == 0):
        i += 43_200

    if (i % 3_600 == 0) or (i > n_muestras - 100):
        valor_avanzado = i/n_muestras * 100
        print(f"Status: {valor_avanzado}%")

print("Finalizado")