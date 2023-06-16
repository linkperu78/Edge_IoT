# Importamos las funciones para generar valores controlados
import mat_function as mat

# Clase base
class id_canbus:
    def __init__(self, id_tag, init_byte, len_byte, min_value):
        self.id_tag = id_tag
        self.init = init_byte
        self.len = len_byte
        # Maximo valor posible
        self.max_value = 2 ** (8*len_byte -1)
        # Minimo valor posible
        self.min_value = min_value
        self.actual_value = min_value
        # Numero de veces que se ha llamado la clase
        self.repeat = 0

    def get_id(self):
        return self.id_tag

    def get_real_value(self, value):
        temp = value
        if temp > self.max_value:
            temp = self.max_value
        if temp < self.min_value:
            temp = self.min_value
        return temp
    
    def get_byte(self, value):
        real = self.get_real_value(value)
        self.repeat += 1
        return self.init, self.len, mat.num_to_byte(real, self.len)

    def set_max_value(self, new_max):
        self.max_value = new_max

# Clase derivada para casos de incremento y decremento
class canbus_cuadratica(id_canbus):
    def __init__(self, id_tag, init_byte, len_byte, min_value, hold = 100, rising = 100):
        super().__init__(id_tag, init_byte, len_byte, min_value)
        # Numero de llamadas que mantiene el min o max
        self.hold = hold
        # Cambio del valor durante el incremento o decremento
        self.rising = rising
        # Numero de veces que se ha llamado la clase
        self.counter = 0

    def get_data(self):
        self.actual_value, self.counter = mat.function_sube_baja(self.hold, self.max_value, self.min_value, 
                                                                 self.rising, self.actual_value, self.counter)
        return self.get_byte(self.actual_value)

# Clase derivada para valores aleatorios con offset
class canbus_white_noise(id_canbus):
    def __init__(self, id_tag, init_byte, len_byte, min_value, off_set, rango_ruido):
        super().__init__(id_tag, init_byte, len_byte, min_value)
        self.rango_ruido = rango_ruido
        self.offset = off_set

    def get_data(self):
        ruido = mat.ruido_blanco(self.offset, self.rango_ruido)
        return self.get_byte(ruido)

# Clase derivada para valores en aumento
class canbus_incremento(id_canbus):
    def __init__(self, id_tag, init_byte, len_byte, min_value, init_value, gain):
        super().__init__(id_tag, init_byte, len_byte, min_value)
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
    def __init__(self, id_tag, init_byte, len_byte, min_value, const_value):
        super().__init__(id_tag, init_byte, len_byte, min_value)
        self.const = const_value
        self.actual_value = self.const

    def get_data(self):
        return self.get_byte(self.const)

# Clase derivada para valores que se reinician tras un tiempo
class canbus_renovacion(id_canbus):
    def __init__(self, id_tag, init_byte, len_byte, min_value, init_value, change_value, restart):
        super().__init__(id_tag, init_byte, len_byte, min_value)
        self.init_value = init_value
        self.actual_value = init_value
        self.change = change_value
        self.restart = restart
        self.counter = 0
        
    def get_data(self):
        if(self.counter < self.restart):
            self.actual_value += self.change
            self.counter += 1
        else:
            self.actual_value = self.init_value
            self.counter = 0

        return self.get_byte(self.actual_value)

# Clase diccionario con los valores de frecuencia de cada TAG
class valores_canbus:
    def __init__(self) :   
        self.actual_byte = [0] * 8

        self.dictionary = {
            "0x0cf00300"    : {
                            'freq' : 60,  
                            'members' : [# Factor de carga de motor 
                                         canbus_white_noise("Fcarga", 3, 1, 0, 100, 50),
                                         # Posición del acelerador
                                         canbus_white_noise("Acelerador", 2, 1, 0, 80, 50)]},
            
            "0x0cf00400"    : {
                            'freq' : 30,
                            'members' : [# Velocidad del motor
                                         canbus_cuadratica("RPM", 4, 2, 8000, 20, 8000),
                                         # Torque actual 
                                         canbus_white_noise("TorqueActual", 3, 1, 10, 10, 20)]}, 
            
            "0x0cfedf00"    : {
                            'freq' : 120,
                            #'freq' : 2,
                            'members' : [# Velocidad Deseada del motor
                                         canbus_cuadratica("RPMDeseado", 2, 2, 8000, 300, 8000),
                                         # Torque requerido 
                                         canbus_white_noise("PTorque", 1, 1, 20, 20, 20)]},
            
            "0x0cfee400"    : {
                            'freq' : 3600,
                            'members' : [# Estado de protección del motor
                                         can_bus_constante("EMotor", 5, 1, 0, 1)]},
            
            "0x0cfee500"    : {
                            'freq' : 3600,
                            'members' : [# Horometro de funcionamiento de motor
                                         canbus_incremento("Horometro", 1, 4, 0, 200000, 20)]},
            
            "0x0cfee900"    : {
                            'freq' : 60,
                            'members' : [# Indicador de nivel de combustible
                                         canbus_renovacion("CCombustible", 5, 4, 0, 6000000, -300, 480)]},
            
            "0x0cfeee00"    : {
                            'freq' : 300,
                            'members' : [# Temperatura Combustible
                                         canbus_white_noise("TCombustible", 2, 1, 0, 90, 10),
                                         # Temperatura Lubricante
                                         canbus_white_noise("TLubricante", 3, 2, 10, 70, 10),
                                         # T del refrigerante del motor
                                         canbus_white_noise("TRefrigerante", 1, 1, 20, 40, 10)]},
            
            "0x0cfeef00"    : {
                            'freq' : 300,
                            'members' : [# P del aceite del motor manométrica
                                         canbus_white_noise("PLubricante", 4, 1, 0, 63, 8),
                                         # Nivel de refrigerante
                                         canbus_renovacion("NRefrigerante", 8, 1, 0, 250, -1, 200),
                                         # Presión manométrica de combustible
                                         canbus_white_noise("PCombustible", 1, 1, 0, 163, 15)]},
            
            "0x0cfef200"    : {
                            'freq' : 120,
                            'members' : [# Caudal de combustible
                                         canbus_white_noise("QCombustible", 1, 2, 0, 125, 20)]},
            
            "0x0cfef500"    : {
                            'freq' : 600,
                            'members' : [# Presión atmosférica
                                         can_bus_constante("PAtmosferica", 1, 1, 200, 202)]},
            
            "0x0cfef600"    : {
                            'freq' : 60,
                            'members' : [# Temperatura del múltiple de admisión
                                         canbus_white_noise("TAdmision", 3, 1, 0, 100, 10),
                                         # Presión del múltiple de admisión
                                         canbus_white_noise("PAdmision", 2, 1, 0, 125, 10),
                                         # Presión a la salida del turbo
                                         canbus_white_noise("PSalida", 1, 1, 0, 125, 10)]},
            
            "0x0cfef700"    : {
                            'freq' : 1200,
                            'members' : [# Voltaje de la batería
                                         canbus_white_noise("Voltaje", 5, 2, 240, 6000, 700)]}
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

