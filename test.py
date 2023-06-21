import funciones as can_lib

my_dictionary = can_lib.id_can_datos

my_list_id = list( my_dictionary.keys() )
my_special_id = can_lib.special_id

my_freq_array = []
for _id in my_list_id:
    # Obtenemos el array de freq de cada TAG
    my_freq_array.append(can_lib.lista_id[_id])
print(my_freq_array)

for pos_tag, freq_array in enumerate(my_freq_array):
    for pos_id, freq in enumerate(freq_array):
        _tag = my_list_id[pos_tag]
        #print(_tag)
        id_class = list(my_dictionary[_tag])[pos_id]
        id_class.set_flag(1)
        print(f"Se ha habilitado el id : {id_class.get_id()}")
