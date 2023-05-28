import time

class tag_config:
    def __init__(self, tag_name, init_byte, len_byte, scale, offset):
        self.tag_name   = tag_name
        self.init_byte  = init_byte
        self.len_byte   = len_byte
        self.scale      = scale
        self.offset     = offset
  
    def get_value_from_can(self, hex_array):
        temp_hex = "0x"
        for i in range(self.len_byte):
            pos = self.init_byte-i+self.len_byte-2
            temp_hex += hex_array[pos]
        return int(temp_hex,16)*self.scale + self.offset
    
    def values_to_pub(self, array_hexadecimal):
        return self.get_value_from_can(array_hexadecimal), self.tag_name
    
class tag_config_bits:
    def __init__(self, tag_name, init_bit, len_bit):
        self.tag_name   = tag_name
        self.init_byte  = init_bit
        self.len_byte   = len_bit

# Diccionario para DATOS SALUD
                    # tag_config("TAG", StartByte, LenByte, Scale, Offset)
id_can_datos = {"f004" : {  tag_config("RPM",4,2,0.125,0),            # 190/
                            tag_config("TorqueActual",3,1,1,-125)    # 513/
                        },
                "fedf":  {  tag_config("RPMDeseado",2,2,0.125,0),       # 515/
                            tag_config("PTorque",1,1,1,-125)           # 514/
                        },
                "f003":  {  tag_config("Fcarga",3,1,1,0),           # 92/
                            tag_config("Acelerador",2,1,0.4,0)        # 91/
                        },
                "fef6":  {  tag_config("TAdmision",3,1,1,-40),        # 105/
                            tag_config("PAdmision",2,1,2,0),        # 102/
                            tag_config("PSalida",4,1,2,0)           # 106/
                        },
                "fee9":  {  tag_config("CCombustible",5,4,0.5,0)      # 250/
                        },
                "feef":  {  tag_config("PLubricante",4,1,4,0),      # 100/
                            tag_config("NRefrigerante",8,1,0.4,0),    # 111/
                            tag_config("PCombustible",1,1,4,0)      # 94/
                        },
                "fef5":  {  tag_config("PAtmosferica",1,1,0.5,0)      # 108/
                        },
                "fef7":  {  tag_config("Voltaje",5,2,0.05,0)           # 168/
                        },
                "feee": {   tag_config("TCombutible",2,1,1,-40),      # 174/
                            tag_config("TLubricante",3,2,0.03125,-273),      # 175/
                            tag_config("TRefrigerante",1,1,1,-40)     # 110/
                        },
                "fee4": {   tag_config_bits("EMotor",5.7,2)     # 1107/
                        },
                "fef2": {   tag_config("QCombustible",1,2,0.05,0)      # 183/
                        },
                }




# Load Rite Sensor      PESAJE 3180
'''
def idFF84(dato): # Eventos
    tipo = int(quitar(dato,7))

    if tipo == 1:
        escala, offset =   1 , -2147483648
        # byte: 3 , largo : 4
        dato = quitar(dato, 2) & 0x0000FFFFFFFF
        dato = voltear4(dato)  
        etiqueta, valor, unidad = "Bucket Event    ", calcular(dato, escala, offset ), 'kg'
    
    if tipo == 2:
        escala, offset =   1 , 0
        # byte: 2 , largo : 4
        dato = quitar(dato, 3)& 0x00FFFFFFFF
        dato = voltear4(dato)  
        etiqueta, valor, unidad = "Vessel Completed", calcular(dato, escala, offset ), 'kg'
    
    if tipo == 3:
        escala, offset =   1 , 0
        # byte: 2 , largo : 4
        dato = quitar(dato, 3)& 0x00FFFFFFFF
        dato = voltear4(dato)  
        etiqueta, valor, unidad = "Truck Completed ", calcular(dato, escala, offset ), 'kg'

    return [dato, valor, etiqueta, unidad]

def idFF83(dato): # Status
    tipo = int(quitar(dato,7))
    if tipo == 0:
        escala, offset =   1 , 0
        # byte: 2 , largo : 1
        dato = quitar(dato, 6) & 0x00FF
        etiqueta, valor, unidad = "Load Cycle      ", calcular(dato, escala, offset ) , '0: start 1: end'   

def idFF81(dato): # Report
    tipo = int(quitar(dato,7))
    if tipo == 130:
        escala, offset =   100 , 0
        # byte: 2 , largo : 1
        dato = quitar(dato, 6) & 0x00FF
        etiqueta, valor, unidad = "Load Cycle      ", calcular(dato, escala, offset ) , '0: start 1: end'  
'''










