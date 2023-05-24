import time

class tag_config:
    def __init__(self, tag_name, init_byte, len_byte, scale, offset):
        self.tag_name   = tag_name
        self.init_byte  = init_byte
        self.len_byte   = len_byte
        self.scale      = scale
        self.offset     = offset
    
    def process_value(self, value):
        scaled_value = value * self.scale + self.offset
        return scaled_value
    
    def get_value_from_can(self, hex_data):
        value = hex_data * self.init_byte - self.len_byte
        return self.process_value(value)
    
    def values_to_pub(self, data_hexadecimal):
        return self.get_value_from_can(data_hexadecimal), self.tag_name


# Diccionario para DATOS SALUD
id_can_datos = {"0x0cf00400" : {tag_config("RPM",1,2,1,0),          # 515
                                tag_config("TorqueActual",3,2,1,0)  # 513
                                },
                "0x0cfedf00":  {tag_config("RPMDeseado",1,2,1,0)    # 515
                                },
                "0x0cf00300":  {tag_config("Fcarga",1,2,1,0)        # 92
                                },
                "0x18fef600":  {tag_config("TAdmision",1,2,1,0),    # 105
                                tag_config("PAdmision",3,2,1,0)     # 106
                                },
                "0x18fef200":  {tag_config("CCombustible",1,2,1,0)  # 183
                                },
                "0x18feef00":  {tag_config("PCombustible",1,2,1,0)  # 94
                                },
                "0x18fee900":  {tag_config("PLubricante",1,2,1,0),  # 100
                                tag_config("NRefrigerante",3,2,1,0) # 111
                                },
                "0x18fef500":  {tag_config("PAtmosferica",1,2,1,0)  # 108
                                },
                "0x18fef700":  {tag_config("Voltaje",1,2,1,0)       # 168
                                },
                "0x18feee00":  {tag_config("TCombutible",1,2,1,0),  # 174
                                tag_config("TLubricante",3,2,1,0),  # 175
                                tag_config("TRefrigerante",3,2,1,0) # 110
                                },
                "0x12121212":  {tag_config("Acelerador",1,2,1,0)    # 91
                                },
                "0x12121213":   {tag_config("PTorque",1,2,1,0)      # 514
                                },
                "0x12121214":  {tag_config("EMotor",1,2,1,0)        # 1107
                                },
                "0x12121215": {tag_config("QCombustible",1,2,1,0)   # 183
                                },
                "0x12121216": {tag_config("PSalida",1,2,1,0)        # 106
                                } 
                }


def quitar(dato, i):
    return (dato >> 8*i)

def agregar(dato, i):
    return (dato << 8*i)

def voltear2(dato):
    dato = agregar(dato & 0x00FF,1) + quitar(dato & 0xFF00,1)
    return dato

def voltear4(dato):
    dato = agregar(dato & 0x000000FF, 3) + agregar(dato & 0x0000FF00, 1) + quitar(dato & 0x00FF0000,1) + quitar(dato & 0xFF000000,3)

def calcular(valor, escala, offset):
    valor = int(valor)*escala + offset 
    valor = round(valor,2)
    return valor

# SCOOP Data  SALUD

def id0CF00400_RPM(dato): # 0x0cf00400       	SPN 515
    escala, offset =   0.125, 0
    #escala, offset =   1, 0   
    # byte: 4 , largo :2    
    #dato = 0xFFFF E10000 FFFFFF 
    dato = quitar(dato,3) & 0x000000FFFF
    dato = voltear2(dato)
    etiqueta, valor, unidad= "RPM", calcular(dato, escala, offset ) , "rpm"
    return [dato, valor, etiqueta, unidad]

def id0CF00400_TOR(dato):  # Torque Actual 	SPN 513
    escala, offset =   1 , -125
    #escala, offset =   1 , 0
    # byte: 3 , largo :1    
    dato = quitar(dato,5) & 0x0000FF
    etiqueta, valor, unidad = "TorqueActual", calcular(dato, escala, offset ), '%'
    return [dato, valor, etiqueta, unidad]

def id0CFEDF00_RPMD(dato):   # RPM Deseado 	SPN 515
    escala, offset =   0.125 , 0
    # byte: 2 , largo :2    
    dato = quitar(dato,5) & 0x00FFFF
    dato = voltear2(dato)
    etiqueta, valor, unidad = "RPMDeseado", calcular(dato, escala, offset ), 'rpm'
    return [dato, valor, etiqueta, unidad]

def id0CF00300_LOAD(dato):   # Factor de carga de motor 	SPN 92
    escala, offset =   1 , 0
    # byte: 3 , largo :1    
    dato = quitar(dato,5) & 0x0000FF
    etiqueta, valor, unidad = "FCarga", calcular(dato, escala, offset ), '%'
    return [dato, valor, etiqueta, unidad]

def id18FEF600_TAD(dato):      # Temperatura de admision 	SPN 105
    escala, offset =   1 , -40
    # byte: 3 , largo :1    
    dato = quitar(dato,5)& 0x0000FF
    etiqueta, valor, unidad = "TAdmision", calcular(dato, escala, offset ), '°C'
    return [dato, valor, etiqueta, unidad]  

def id18FEF600_PAD(dato):      # Presio de admision 		SPN 106
    escala, offset =   2 , 0
    # byte: 4 , largo :1    
    dato = quitar(dato,4)& 0x000000FF
    etiqueta, valor, unidad = "PSalida", calcular(dato, escala, offset ), 'Pa'

def id18FEF200_COMB(dato):     # Caudal de Combustible  	SPN 183
    escala, offset =   0.05 , 0
    # byte: 1 , largo :2  
    dato = quitar(dato,6)
    dato = voltear2(dato)  
    etiqueta, valor, unidad = "CCombustible", calcular(dato, escala, offset ), 'L/h'  
    return [dato, valor, etiqueta, unidad]  

def id18feef00_PCOMB(dato):  # Presión manométrica del combustible SPN 94
    escala, offset =   4 , 0
    # byte: 1 , largo :1  
    dato = quitar(dato,7)  
    etiqueta, valor, unidad = "PCombustible", calcular(dato, escala, offset ), 'kPa'  
    return [dato, valor, etiqueta, unidad]  

def id18FEE900_TLU(dato):   # P manométrica del aceite del motor  SPN 100
    escala, offset =   4 , 0
    # byte: 4 , largo : 1    
    dato = quitar(dato,4) & 0x000000FF
    etiqueta, valor, unidad = "PLubricante", calcular(dato, escala, offset ), 'kPa'
    return [dato, valor, etiqueta, unidad]

def id18FEE900_NRE(dato):   # Nivel de Refrigerante   SPN 111
    escala, offset =   0.4 , 0
    # byte: 8 , largo : 1    
    dato = dato & 0x00000000000000FF
    etiqueta, valor, unidad = "NRefrigerante", calcular(dato, escala, offset ), '%'
    return [dato, valor, etiqueta, unidad]

def id18FEF500_PATM(dato):   # Presión Atmosférica SPN 108
    escala, offset =   0.5 , 0
    # byte: 1 , largo : 1  
    dato = quitar(dato,7) 
    etiqueta, valor, unidad = "PAtmosferica", calcular(dato, escala, offset ), 'kPa'
    return [dato, valor, etiqueta, unidad]  

def id18FEF700_VBAT(dato):   #  Voltaje de batería   SPN 168 
    escala, offset =   0.05 , 0
    # byte: 5 , largo : 2
    dato =  quitar(dato,2) & 0x000000FFFF
    dato = round(voltear2(dato),2)
    etiqueta, valor, unidad = "Voltaje", calcular(dato, escala, offset ), 'V'
    return [dato, valor, etiqueta, unidad]  

def id18FEEE00_TCOMB(dato):  # T del combustible SPN 174
    escala, offset =   1 , -40
    # byte: 2 , largo : 1
    dato = quitar(dato, 6)  & 0x00FF
    etiqueta, valor, unidad = "TCombustible", calcular(dato, escala, offset ), '°C'
    return [dato, valor, etiqueta, unidad]  

def id18FEEE00_TACE(dato):  # T lubricante   SPN 175
    escala, offset =   0.03125 , -273
    # byte: 3, largo : 2
    dato = quitar(dato, 4)  & 0x0000FFFF
    dato = voltear2(dato)
    etiqueta, valor, unidad = "TLubricante", calcular(dato, escala, offset ), '°C'
    return [dato, valor, etiqueta, unidad]  

def id18FEEE00_TREF(dato):  # T del refrigerante SPN 110
    escala, offset =   1 , -40
    # byte: 1 , largo : 1
    dato = quitar(dato, 7)  
    etiqueta, valor, unidad = "TRefrigerante", calcular(dato, escala, offset ), '°C'
    return [dato, valor, etiqueta, unidad]  

# Agregar Acelerador
# Agregar PTorque
# Agregar IndicadorCombustible


# Load Rite Sensor      PESAJE 3180

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
 










