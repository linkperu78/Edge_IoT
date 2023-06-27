# Definimos la lista de variables a decodificar con su respectiva frecuencia deseada:
list_tag = {
    # TAG   :   [Init byte, len_byte, scale, offset, freq]
    "RPM"           :   [4, 2,      0.125, 0,       50],
    #"RPM"           :   [4, 2,      0.125, 0,       30],
    "TorqueActual"  :   [3, 1,      1, -125,        60000],
    "RPMDeseado"    :   [2, 2,      0.125, 0,       50],
    #"RPMDeseado"    :   [2, 2,      0.125, 0,       120],
    "PTorque"       :   [1, 1,      1, -125,        60000],
    "Fcarga"        :   [3, 1,      1, 0,           120],
    "Acelerador"    :   [2, 1,      0.4, 0,         50],
    "TAdmision"     :   [3, 1,      1, -40,         150], #600],
    "PAdmision"     :   [2, 1,      2, 0,           150], #60],
    "PSalida"       :   [4, 1,      2, 0,           150], #120],
    "CCombustible"  :   [5, 4,      0.5, 0,         100], #60],
    "PLubricante"   :   [4, 1,      4, 0,           100], #6000],
    "NRefrigerante" :   [8, 1,      0.4, 0,         100], #1200],
    "PCombustible"  :   [1, 1,      4, 0,           100], #300],
    "PAtmosferica"  :   [1, 1,      0.5, 0,         300], #600],
    "Voltaje"       :   [5, 2,      0.05, 0,        200], # 1200],
    "TCombustible"  :   [2, 1,      1, -40,         100], # 300],
    "TLubricante"   :   [3, 2,      0.03125, -273,  60000], # 6000],
    "TRefrigerante" :   [1, 1,      1, -40,         100], # 1200],
    # EMotor es un caso especial: Inicia 5 byte y toma los dos ultimos bits
    # El -4 quiere indicar que tomaremos el resto del scale
    "EMotor"        :   [5, 1,      -4, 0,          60000], # 3600],
    "QCombustible"  :   [1, 2,      0.05, 0,        50], # 120] ,
    "Horometro"     :   [1, 4,      0.05, 0,        50], # 3600]
}

array_id = ["f004", "fedf", "f003", "fef6", "fee9", "feef", "fef5", "fef7", "feee", "fee4", "fef2", "fee5"]

especial_id = ["RPM", "RPMDeseado"]
dic_value = {
    "RPM" : 100,
    "RPMDeseado" : 100,
}

my_tag = [
         ["RPM", "TorqueActual"], 
         ["RPMDeseado","PTorque"],
         ["Fcarga", "Acelerador"],
         ["TAdmision", "PAdmision", "PSalida"],
         ["CCombustible"],
         ["PLubricante", "NRefrigerante", "PCombustible"],
         ["PAtmosferica"],
         ["Voltaje"],
         ["TCombustible", "TLubricante", "TRefrigerante"],
         ["EMotor"],
         ["QCombustible"],
         ["Horometro"]
]

