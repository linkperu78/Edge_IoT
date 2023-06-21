# Clase para datos que son formados por bytes
class tag_config:
    def __init__(self, tag_name, init_byte, len_byte, scale, offset):
        self.tag_name   = tag_name
        self.init_byte  = init_byte
        self.len_byte   = len_byte
        self.scale      = scale
        self.offset     = offset
        self.actual_value = 0
        self.change_needed = 0.03 * ( ( 2 ** len_byte ) * scale - offset )
        self.flag = 1

    def get_id(self):
        return self.tag_name

    def get_flag(self):
        return self.flag

    def set_flag(self, value):
        self.flag = value

    def is_new_value(self, input_value):
        # Retornamos 1 si el valor es sustancialmente diferente
        # Retornamos 0 para ignorar el valor entrante
        if ( abs(input_value - self.actual_value) >  self.change_needed):
            self.actual_value = input_value
            return 1
        else:
            return 0

    # Convertimos los bytes correspondientes a un valor entero segun TAG
    def get_value_from_can(self, hex_array):
        temp_hex = "0x"
        for i in range(self.len_byte):
            pos = self.init_byte-i+self.len_byte-2
            temp_hex += hex_array[pos]
        return int(temp_hex,16)*self.scale + self.offset
    
    # Obtenemos el array: [ Tag_Value, "Tag_name" ]
    def values_to_pub(self, array_hexadecimal):
        array = [self.get_value_from_can(array_hexadecimal), self.tag_name]
        return array
    

# Clase para datos que solo forman bits    
class tag_config_bits:
    def __init__(self, tag_name, init_bit, len_bit, dictionary):
        self.tag_name   = tag_name
        self.init_byte  = init_bit
        self.len_byte   = len_bit
        self.dict       = dictionary
        self.flag       = 1

    def get_id(self):
        return self.tag_name

    def get_flag(self):
        return self.flag

    def set_flag(self, value):
        self.flag = value

    # Obtenemos el array: [ Tag_Value, "Tag_name" ] 
    def values_to_pub(self, hex_array):
        hex_value = ""

        for i in range(len(hex_array)):
            hex_value += hex_array[i]

        bin_value = bin(int(hex_value,16))
        bin_value = str(bin_value)[2:]
        int_byte = int(self.init_byte)
        dot_byte = (self.init_byte - int_byte)*10
        real_bit = int(int_byte *8 + dot_byte) 
        k_bin = bin_value[real_bit-1:real_bit-1+self.len_byte]
        pos_dict = int(k_bin,2)

        return [self.dict[pos_dict], self.tag_name]



# Definimos la lista de variables a decodificar con su respectiva frecuencia deseada:

array_id   = ["f004", "fedf", "f003", "fef6", "fee9", "feef", "fef5", "fef7", "feee", "fee4", "fef2", "fee5"]
#array_id = []

special_id = ["f004", "fedf"]
#special_id = ["f004"]

lista_id = {
    array_id[0] :   [30, 30],           #   RPM, TorqueActual
    array_id[1] :   [120, 120],         #   RPMDeseado, PTorque
    array_id[2] :   [60, 60],           #   Fcarga, Acelerador
    array_id[3] :   [60, 60],           #   TAdmision, PAdmision, PSalida
    array_id[4] :   [60],               #   CCombustible
    array_id[5] :   [300, 300, 300],    #   PLubricante, NRefrigerante, PCombustible
    array_id[6] :   [600],              #   PAtmosferica
    array_id[7] :   [1200],             #   Voltaje
    array_id[8] :   [300, 300, 300],    #   TCombustible, TLubricante, TRefrigerante
    array_id[9] :   [3600],             #   EMotor
    array_id[10] :  [120],              #   QCombustible
    array_id[11] :  [3600],             #   Horometro
}


# Diccionario para DATOS SALUD
# Usaremos este diccionario para extraer los datos a publicar
# Segun el mensaje CAN que llega
                    # tag_config("TAG", StartByte, LenByte, Scale, Offset)
id_can_datos = {array_id[0] :   { 
                                tag_config("RPM", 4, 2, 0.125, 0),            # 190/
                                tag_config("TorqueActual", 3, 1, 1, -125)    # 513/
                                },

                array_id[1] :   { 
                                tag_config("RPMDeseado",2,2,0.125,0),       # 515/
                                tag_config("PTorque",1,1,1,-125)           # 514/
                                },

                array_id[2] :   { 
                                tag_config("Fcarga",3,1,1,0),           # 92/
                                tag_config("Acelerador",2,1,0.4,0)        # 91/
                                },

                array_id[3] :   {  
                                tag_config("TAdmision",3,1,1,-40),        # 105/
                                tag_config("PAdmision",2,1,2,0),        # 102/
                                tag_config("PSalida",4,1,2,0)           # 106/
                                },

                array_id[4] :   {  
                                tag_config("CCombustible",5,4,0.5,0)      # 250/
                                },

                array_id[5] :   {  
                                tag_config("PLubricante",4,1,4,0),      # 100/
                                tag_config("NRefrigerante",8,1,0.4,0),    # 111/
                                tag_config("PCombustible",1,1,4,0)      # 94/
                                },

                array_id[6] :   {  
                                tag_config("PAtmosferica",1,1,0.5,0)      # 108/
                                },

                array_id[7] :   {  
                                tag_config("Voltaje",5,2,0.05,0)           # 168/
                                },

                array_id[8] :   {
                                tag_config("TCombutible",2,1,1,-40),      # 174/
                                tag_config("TLubricante",3,2,0.03125,-273),      # 175/
                                tag_config("TRefrigerante",1,1,1,-40)     # 110/
                                },

                array_id[9] :   {
                                tag_config_bits("EMotor", 5.7, 2, [1,2,3,4] )     
                                },
                                                                                                                          # 1107/
                array_id[10] :   {
                                tag_config("QCombustible",1,2,0.05,0)      # 183/
                                },

                array_id[11] :   {
                                tag_config("Horometro",1,4,0.05,0)      # 247/
                                }
                }


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


'''
def save_data(data, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as file:
        if file_exists:
            file.write('\n')
        file.write(data)

def get_data_backup():
    name_file = "back_up.json"
    path = "json_data/" + name_file
    with open(path,'r') as file:
        json_data = json.load(file)
    return json_data['state'],json_data['date']
    
def get_time_last_date():
    name_file = "last_date.txt"
    path = "json_data/" + name_file
    with open(path,'r') as file:
        number = file.read()
    print(number)
'''
