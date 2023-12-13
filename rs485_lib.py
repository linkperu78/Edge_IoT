import json
from crc16_table import crc16_table


def get_json_from_file(json_file):
    extension = ".json"
    path = json_file
    if not (extension in json_file):
        path = json_file.split(".")[0]
        path = path + extension
    with open("json_values/" + path, 'r') as file:
        return json.load(file)
    
def save_in_json_file(json_file, data):
    extension = ".json"
    path = json_file
    if not (extension in json_file):
        path = json_file.split(".")[0]
        path = path + extension
    path = "json_values/" + path
    with open(path, 'w') as file:
        json.dump(data, file)

def convert_decimal_hexarray(decimal_value : int):
    #if decimal_value > 125:
        #return 0x00, 0x00
    hex_array = []
    for _ in range(2):
        hex_array.append(int (decimal_value % 256))
        decimal_value = int(decimal_value / 256)
    return hex_array[::-1]


class cdl_rs485:
    def __init__(self, json_file : str):
        self.r1300g_dictionary  = get_json_from_file(json_file)

    def get_array_id(self):
        return self.r1300g_dictionary.keys()

    def get_basic_dictionary(self):
        new_dictionary = {}
        my_keys_array = self.get_array_id()
        for key in my_keys_array:
            freq_new = self.r1300g_dictionary[key]["freq"]
            register = self.r1300g_dictionary[key]["Registro"]
            new_dictionary[key] = {
                "freq" : freq_new,
                "reg"  : register
            }
        return new_dictionary

    def crc_rs485_calculator(self, byte_message):
        def invert_2_bytes(hex_2_bytes):
            first_byte = hex_2_bytes % 256
            second_byte =  int (hex_2_bytes / 256)
            return first_byte * 256 + second_byte 
        crc = 0xFFFF  # Initial value for CRC-16
        for byte in byte_message:
            pos_table = ( byte ^ crc ) & 0xFF
            crc = int(crc / 256)
            crc ^= crc16_table[pos_table]
        return invert_2_bytes(crc)  # Ensure CRC-16 is a 16-bit value

    def rs485_request(self, id_dispositivo : int, registro_inicio : int, registo_final : int ):
        rs485_message   = [id_dispositivo]
        rs485_message   += [0x03]
        rs485_message   += convert_decimal_hexarray(registro_inicio)
        len_registro    = registo_final - registro_inicio + 1
        rs485_message   += convert_decimal_hexarray(len_registro)
        rs485_message   += convert_decimal_hexarray(self.crc_rs485_calculator(rs485_message))
        return rs485_message
        




