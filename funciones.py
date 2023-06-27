import estructura_can


# Clase para datos que son formados por bytes
class base_config:
    def __init__(self, tag_name, init_byte, len_byte, scale, offset, freq):
        self.tag_name   = tag_name
        self.init_byte  = init_byte
        self.len_byte   = len_byte
        self.scale      = scale
        self.offset     = offset
        self.freq       = freq
        self.time_prev  = 0
        self.value      = 0
    
    def get_id(self):
        return self.tag_name

    # Convertimos los bytes correspondientes a un valor entero segun TAG
    def get_value_from_can(self, hex_array):
        temp_hex = "0x"
        for i in range(self.len_byte):
            pos = self.init_byte-i+self.len_byte-2
            temp_hex += hex_array[pos]
        raw_value = int(temp_hex, 16)
        if(self.scale < 0):
            raw_value = raw_value % abs(self.scale)
            return raw_value + self.offset
        return raw_value * self.scale + self.offset
    

class tag_config(base_config):
    def __init__(self, tag_name, init_byte, len_byte, scale, offset, freq):
        super().__init__(tag_name, init_byte, len_byte, scale, offset, freq)

    # Obtenemos el array: [ Tag_Value, "Tag_name" ]
    def values_to_pub(self, array_hexadecimal, time_pass):
        value = self.get_value_from_can(array_hexadecimal)
        flag = time_pass % self.freq
        #print(f"Time: {self.time_prev} /  {time_pass} - freq = {self.freq} - flag = {flag}")
        if flag == 0 and self.time_prev < time_pass :
            self.time_prev = time_pass
            return [value, self.tag_name ]
        return None


class special_tag_config(base_config):
    def __init__(self, tag_name, init_byte, len_byte, scale, offset, freq, change_value):
        super().__init__(tag_name, init_byte, len_byte, scale, offset, freq)
        self.change = change_value
    
    # Obtenemos el array: [ Tag_Value, "Tag_name" ]
    def values_to_pub(self, array_hexadecimal, time_pass):
        # Si el valor es mayor al almanecado por la cantidad suficiente
        # Guardamos el nuevo valor y habilitamos el flag para su envio
        value = self.get_value_from_can(array_hexadecimal)
        if( abs(self.value - value) > self.change ):
            self.value = value
            return [value , self.tag_name ]
        if time_pass % self.freq == 0 and self.time_prev < time_pass :
            self.time_prev = time_pass
            return [self.value, self.tag_name ]
        return None


# Creamos un constructor de diccionarios
def create_dictionary():
    my_tag = estructura_can.my_tag
    list_tag = estructura_can.list_tag
    array_id = estructura_can.array_id
    
    base_dictionary = {
    }
    pos_tag = 0
    for tag in array_id:
        #print(f"Tag = {tag}")
        class_array = []
        array_id = my_tag[pos_tag]
        #print(f"Array_id = {array_id}")
        for id in array_id:
            #print(f"ID = {id}")
            _init, _len, _scale, _offset, _freq = list_tag[id]
            #_freq = int( _freq / 10 )
            if id in estructura_can.especial_id:
                change_value = estructura_can.dic_value[id]
                new_class = special_tag_config(id, _init, _len, _scale, _offset, _freq, change_value)
            else:
                new_class = tag_config(id, _init, _len, _scale, _offset, _freq)
            class_array.append(new_class)
        base_dictionary[tag] = class_array
        pos_tag += 1
    
    return base_dictionary


def get_matrix_freq():
    my_tag = estructura_can.my_tag
    list_tag = estructura_can.list_tag
    matrix_freq = []
    for array_tag in my_tag:
        array = []
        for tag in array_tag:
            array_freq = list_tag[tag]
            array_freq = array_freq[-1]
            array_freq = int( array_freq / 10 )
            array.append(array_freq)
        matrix_freq.append(array)
    return matrix_freq


def get_matrix_tag():
    return estructura_can.my_tag


def get_array_tag():
    return estructura_can.array_id


# parameters: "Mensaje completo de can_bus "
# return: timestamp , tag, data_byte
def get_data_canbus(msg_canbus):
    data_canbus_str = []
    i, time, id, pos_data = 0,"","",0
    temp = msg_canbus.split()
    len_temp = len(temp)

    while i < len_temp:
        new_temp = temp[i]
        if new_temp == "Timestamp:":
            i += 1
            time = temp[i]
            continue
        if new_temp == "ID:":
            i += 1
            id = temp[i][2:6]
            continue
        if new_temp == "DL:":
            i += 1
            pos_data = int(temp[i])
            for j in range(pos_data):
                data_canbus_str.append(temp[j+i+1])
            break; 
        i += 1
    return [time, id, data_canbus_str]

