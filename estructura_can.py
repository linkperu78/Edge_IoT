# Definimos la lista de variables a decodificar con su respectiva frecuencia deseada:
salud_paremeters_id = {
    # TAG   :   [Init byte, len_byte, scale, offset, freq, change_value, max_value, min_value]
        # RPM           = 0 - 8 031.875 rpm
    "RPM"           :   [4, 2,      0.125, 0,       30, 250,        0, 3000],
        # TorqueActual  = 0 - 125%
    "TorqueActual"  :   [3, 1,      1, -125,        60, 2],
        # RPMDeseado    = 0 - 8 031.875 rpm
    "RPMDeseado"    :   [2, 2,      0.125, 0,       120, 250],
        # PTorque       = -125 - 125 %
    "PTorque"       :   [1, 1,      1, -125,        120, 6],
        # Fcarga        = 0 - 125 %
    "Fcarga"        :   [3, 1,      1, 0,           120, 6],
        # Acelerador    = 0 - 100 %
    "Acelerador"    :   [2, 1,      0.4, 0,         60, 5],
        # TAdmision     = -40 - 210 C
    "TAdmision"     :   [3, 1,      1, -40,         600, 10,        0, 90],
        # PAdmision     = 0 - 500 kPa
    "PAdmision"     :   [2, 1,      2, 0,           60, 10,         0, 250],
        # PSalida       = 0 - 500 kPa
    "PSalida"       :   [4, 1,      2, 0,           120, 10,        0, 300],
        # CCombustible  = 0 - 2 105 540 607.5 L
    "CCombustible"  :   [5, 4,      0.5, 0,         60, 1,          0, 2_105_540_607],
        # PLubricante   = 0 - 1000 kPa
    "PLubricante"   :   [4, 1,      4, 0,           300, 20,        100, 500],
        # NRefrigerante = 0 - 100 %
    "NRefrigerante" :   [8, 1,      0.4, 0,         100],
        # PCombustible  = 0 - 1000 kPa
    "PCombustible"  :   [1, 1,      4, 0,           100],
        # PAtmosferica  = 0 - 125 kPa
    "PAtmosferica"  :   [1, 1,      0.5, 0,         300],
        # Voltaje       = 0 - 3 212.75 V
    "Voltaje"       :   [5, 2,      0.05, 0,        200],
        # TCombustible  = -40 - 210 C
    "TCombustible"  :   [2, 1,      1, -40,         100],
        # TLubricante   = -273 - 1 734.968 75 C
    "TLubricante"   :   [3, 2,      0.03125, -273,  60000],
        # TRefrigerante = -40 - 210 C
    "TRefrigerante" :   [1, 1,      1, -40,         100],
    
    # EMotor es un caso especial: Inicia 5 byte y toma los dos ultimos bits
    # El -4 quiere indicar que tomaremos el resto del scale
    "EMotor"        :   [5, 1,      -4, 0,          60000],
        # QCombustible  = 0 - 3 212.75 L/h
    "QCombustible"  :   [1, 2,      0.05, 0,        50],
    }

canbus_salud_list = {
    "f004" : ["RPM", "TorqueActual"], 
    "fedf" : ["RPMDeseado","PTorque"],
    "f003" : ["Fcarga", "Acelerador"],
    "fef6" : ["TAdmision", "PAdmision", "PSalida"],
    "fee9" : ["CCombustible"],
    "feef" : ["PLubricante", "NRefrigerante", "PCombustible"],
    "fef5" : ["PAtmosferica"],
    "fef7" : ["Voltaje"],
    "feee" : ["TCombustible", "TLubricante", "TRefrigerante"],
    "fee4" : ["EMotor"],
    "fef2" : ["QCombustible"],
    }

canbus_pesaje_list = {
    "ff84" : "Evento", 
    "ff83" : "Status Change",
    "ff81" : "Report"
    }

especial_id = {"RPM" : "100", 
               "RPMDeseado" : "100",}


