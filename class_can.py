# Importamos las funciones para generar valores controlados
import mat_function as mat

# Clase base
class id_canbus:
    def __init__(self, id_parametro, init_byte, len_byte, scale, offset):
        self.id = id_parametro
        self.init = init_byte
        self.len = len_byte
        self.scale = scale
        self.offset = offset
        # Maximo valor posible
        self.max_value = 2 ** (8*len_byte) - 1

    def get_id(self):
        return self.id

    # Retornamos el byte correspondiente (NO los 8 bytes)
    def get_byte(self, value):
        desire_value = int( (value - self.offset) / self.scale )

        a = max(desire_value, 0)
        real_value = min(self.max_value, a)
        
        if (desire_value != real_value):
            print(f" WARNING! : {self.id} recieved an off limits value")
        return self.init, self.len, mat.num_to_byte(real_value, self.len)



# Clase derivada para casos de incremento y decremento
class canbus_cuadratica(id_canbus):
    def __init__(self, id_tag, init_byte, len_byte, scale, offset, 
                 min_value, max_value, 
                 n_hold_low, n_hold_high,  
                 change_value):
        super().__init__(id_tag, init_byte, len_byte, scale, offset)
        # Numero de llamadas que mantiene en min
        self.hold_min = n_hold_low
        # Numero de llamadas que mantiene en max
        self.hold_max = n_hold_high
        # Cambio del valor durante el incremento o decremento
        self.change = change_value
        # Numero de veces que se ha llamado la clase
        self.counter = 0
        # Valor Minimo
        self.min = min_value
        # Valor Maximo
        self.max = max_value

    def get_data(self):
        self.actual_value = mat.function_sube_baja(self.min, self.max, self.change, self.counter,
                                                                 self.hold_max, self.hold_min)
        self.counter += 1
        return self.get_byte(self.actual_value)

# Clase derivada para valores aleatorios con offset
class canbus_white_noise(id_canbus):
    def __init__(self, id_tag, init_byte, len_byte, scale, offset,
                 main_value, noise_range ):
        super().__init__(id_tag, init_byte, len_byte, scale, offset)
        self.rango_ruido = noise_range
        self.main_value = main_value

    def get_data(self):
        try:
            ruido = mat.ruido_blanco(self.main_value, self.rango_ruido)
            return self.get_byte(ruido)
        except Exception:
            print(f"Error en {self.get_id()}") 
        
        



# Clase derivada para valores en aumento
class canbus_incremento(id_canbus):
    def __init__(self, id_tag, init_byte, len_byte, scale, offset,
                 init_value, gain ):
        super().__init__(id_tag, init_byte, len_byte, scale, offset)
        self.gain = gain
        self.actual_value = init_value
        
    def get_data(self):
        self.actual_value = mat.slope_rising(self.actual_value, self.gain)
        self.actual_value = min(self.actual_value,self.max_value)
        self.actual_value = max(self.actual_value, self.min_value)
        #return self.actual_value
        return self.get_byte(self.actual_value)
    

    
# Clase derivada para valores constantes
class can_bus_constante(id_canbus):
    def __init__(self, id_tag, init_byte, len_byte, scale, offset,
                 const_value):
        super().__init__(id_tag, init_byte, len_byte, scale, offset)
        self.const = const_value

    def get_data(self):
        return self.get_byte(self.const)



# Clase derivada para valores que se reinician tras un tiempo
class canbus_renovacion(id_canbus):
    def __init__(self, id_tag, init_byte, len_byte, scale, offset,
                 init_value, change_value, restart):
        super().__init__(id_tag, init_byte, len_byte, scale, offset)
        self.value = init_value
        self.init_value = init_value
        self.change = change_value
        self.restart = restart
        self.counter = 0
        
    def get_data(self):
        if(self.counter < self.restart):
            self.value += self.change
            self.counter += 1
        else:
            self.value = self.init_value
            self.counter = 0

        return self.get_byte(self.value)



# Clase diccionario con los valores de frecuencia de cada TAG
class valores_canbus:
    def __init__(self) :   
        self.actual_byte = [0] * 8
        self.dictionary = {
            "0x0cf00300"    : {
                            'freq' : 60,  
                            'members' : [# Factor de carga de motor 
                                         canbus_white_noise("Fcarga", 3, 1, 1, 0, 
                                                            20, 10),
                                         # Posición del acelerador
                                         canbus_cuadratica("Acelerador", 2, 1, 0.4, 0,
                                                            0, 30, 100, 100, 2)
                                        ]},
            "0x0cf00400"    : {
                            'freq' : 30,
                            'members' : [# Velocidad del motor
                                         canbus_cuadratica("RPM", 4, 2, 0.125, 0, 
                                                           600, 2300, 60, 100, 5),
                                         # Torque actual 
                                         canbus_white_noise("TorqueActual", 3, 1, 1, -125,
                                                             6, 5)
                                         ]}, 
            "0x0cfedf00"    : {
                            'freq' : 120,
                            'members' : [# Velocidad Deseada del motor
                                         canbus_cuadratica("RPMDeseado", 2, 2, 0.125, 0, 
                                                           600, 2300, 60, 100, 5),
                                         # Torque requerido 
                                         canbus_white_noise("PTorque", 1, 1, 1, -125,
                                                            20,5)
                                         ]},
            "0x0cfee400"    : {
                            'freq' : 3600,
                            'members' : [# Estado de protección del motor
                                         can_bus_constante("EMotor", 5, 1, 1, 0,
                                                            1)
                                         ]},
            "0x0cfee900"    : {
                            'freq' : 60,
                            'members' : [# Indicador de nivel de combustible
                                         canbus_renovacion("CCombustible", 5, 4, 0.5, 0, 
                                                           14565, 12, 2300)
                                        ]},
            "0x0cfeee00"    : {
                            'freq' : 300,
                            'members' : [# Temperatura Combustible
                                         canbus_white_noise("TCombustible", 2, 1, 1, -40,
                                                             70, 30),
                                         # Temperatura Lubricante
                                         canbus_white_noise("TLubricante", 3, 2, 0.03125, -273,
                                                             40, 10),
                                         # T del refrigerante del motor
                                         canbus_white_noise("TRefrigerante", 1, 1, 1, -40,
                                                             20, 30)
                                        ]},
            "0x0cfeef00"    : {
                            'freq' : 300,
                            'members' : [# P del aceite del motor manométrica
                                         canbus_white_noise("PLubricante", 4, 1, 4, 0,
                                                             100, 12),
                                         # Nivel de refrigerante
                                         canbus_renovacion("NRefrigerante", 8, 1, 0.4, 0,
                                                           50, 3, 780),
                                         # Presión manométrica de combustible
                                         canbus_white_noise("PCombustible", 1, 1, 4, 0,
                                                             120, 30)
                                        ]},
            "0x0cfef200"    : {
                            'freq' : 120,
                            'members' : [# Caudal de combustible
                                         canbus_cuadratica("QCombustible", 1, 2, 0.05, 0,
                                                            0, 60, 100, 100, 1)
                                        ]},
            "0x0cfef500"    : {
                            'freq' : 600,
                            'members' : [# Presión atmosférica
                                         can_bus_constante("PAtmosferica", 1, 1, 0.5, 0, 
                                                           104)
                                        ]},
            "0x0cfef600"    : {
                            'freq' : 60,
                            'members' : [# Temperatura del múltiple de admisión
                                         canbus_white_noise("TAdmision", 3, 1, 1, -40,
                                                            30, 5),
                                         # Presión del múltiple de admisión
                                         canbus_white_noise("PAdmision", 2, 1, 2, 0,
                                                            50, 15),
                                         # Presión a la salida del turbo
                                         canbus_white_noise("PSalida", 1, 1, 2, 0,
                                                            50, 15)
                                        ]},
            "0x0cfef700"    : {
                            'freq' : 1200,
                            'members' : [# Voltaje de la batería
                                         canbus_white_noise("Voltaje", 5, 2, 0.05, 0, 
                                                            30, 3)
                                        ]}
        }

    def get_all_data(self):
        return self.dictionary
    
    def actualizar_valor(self, tag):
        actual_byte = [255] * 8
        for id_can in  self.dictionary[tag]['members']:
            #print(f"CAN- {id_can.get_id()}")
            _pos, _len, temp_data = id_can.get_data()
            #print(f"Posicion inicial: {_pos} - Longitud: {_len} - {temp_data}")
            for i in range(_len):
                actual_byte[_pos + i -1] = temp_data[i]
        self.actual_byte = actual_byte
        return self.actual_byte
        #print(actual_byte)

