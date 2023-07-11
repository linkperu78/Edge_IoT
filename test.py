import class_can as my_class
import time
import can


time_sleep = 0.0001

can_port = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

canbus = my_class.valores_canbus()
array_frecuencias = []
array_tags = []

for key in canbus.dictionary.keys():
    array_tags.append(key)
    array_frecuencias.append(canbus.dictionary[key]['freq'])

i = 1
n_muestras = 2_592_000
my_actual_time = int(time.time()) + 86_400


while i < n_muestras:
    try:
        if( i % 100 == 0):
            #print("Llamamos a la funcion flush")
            can_port.flush_tx_buffer()

        for nu,freq in enumerate(array_frecuencias):
            if ( i % freq == 0):
                tag = array_tags[nu]
                byte_can = canbus.actualizar_valor(tag)
                
                msg = can.Message(
                	arbitration_id = int(tag,16),
                	data=byte_can,
                	is_extended_id = True,
                	timestamp = my_actual_time
                )
                can_port.send(msg)
                #print(msg)
        my_actual_time += 1
        #print( "Iteracion = " + str(i) )
        i += 1
        time.sleep(time_sleep)
        
    except Exception as e:
        #can_port.flush_tx_buffer()
        print( "Error :" + str(e) )
        #if ( str(e) == "Transmit buffer full"):
            #can_port.flush_tx_buffer()
            #print("----------")
    
    if i % 28_800 == 0 :
        i += 43_200

    if (i % 3_600 == 0) or (i > n_muestras - 100):
        valor_avanzado = round( i/n_muestras * 100, 2 )
        print(f" ------- Status: {valor_avanzado}% ------- ")


print("Finalizado")
