import matplotlib.pyplot as plt
import my_sql as sql
import numpy as np
import models as M
# Definimos la lista de variables a decodificar con su respectiva frecuencia deseada:

tag_name = "RPM"

# Funciones para manejar creacion, chequeo o eliminacion
#Creacion de clases
my_db = sql.my_table_functions(M.Salud)

values = my_db.get_data_from(tag_name)
t_axis_time = my_db.get_data_timestamp(tag_name)

axis_time = [int(float(x))%(3600*24) for x in t_axis_time]

t_value = []
y_value = []

for i, time in enumerate(axis_time):
    #continue
    if time > 1700 and time < 3000 :
        y_value.append(values[i])
        t_value.append(axis_time[i])

n_rows = 2
n_cols = 1
fig, axes = plt.subplots( nrows= n_rows, ncols= n_cols)
min_y = round(min(y_value)*0.9 / 200) * 200
max_y = int( max(y_value) * 1.1 )
max_first = 3000

# First row
axes[0].plot(axis_time, values)
axes[0].set_xlabel("Total time span")
axes[0].set_ylabel("Total Value")
axes[0].set_title(f"{tag_name}")
axes[0].set_ylim([0, max_first])
axes[0].set_yticks( np.arange( 0, max_first, 200 ) )

# Plot data on subplots
axes[1].plot(t_value, y_value)  
axes[1].set_xlabel('Timestamp (s)')
axes[1].set_ylabel('Value')
axes[1].set_title(f'{tag_name}')
axes[1].set_yticks( np.arange( min_y, max_y, 200 ) )

plt.show()


'''
list_tag = {
    # TAG   :   [Init byte, len_byte, scale, offset, freq]
    "RPM"           :   [4, 2,      0.125, 0,       10],
    #"RPM"           :   [4, 2,      0.125, 0,       30],
    "TorqueActual"  :   [3, 1,      1, -125,        60],
    "RPMDeseado"    :   [2, 2,      0.125, 0,       10],
    #"RPMDeseado"    :   [2, 2,      0.125, 0,       120],
    "PTorque"       :   [1, 1,      1, -125,        120],
    "Fcarga"        :   [3, 1,      1, 0,           120],
    "Acelerador"    :   [2, 1,      0.4, 0,         60],
    "TAdmision"     :   [3, 1,      1, -40,         600],
    "PAdmision"     :   [2, 1,      2, 0,           60],
    "PSalida"       :   [4, 1,      2, 0,           120],
    "CCombustible"  :   [5, 4,      0.5, 0,         60],
    "PLubricante"   :   [4, 1,      4, 0,           300],
    "NRefrigerante" :   [8, 1,      0.4, 0,         1200],
    "PCombustible"  :   [1, 1,      4, 0,           300],
    "PAtmosferica"  :   [1, 1,      0.5, 0,         600],
    "Voltaje"       :   [5, 2,      0.05, 0,        1200],
    "TCombustible"  :   [2, 1,      1, -40,         300],
    "TLubricante"   :   [3, 2,      0.03125, -273,  300],
    "TRefrigerante" :   [1, 1,      1, -40,         1200],
    # EMotor es un caso especial: Inicia 5 byte y toma los dos ultimos bits
    # El -4 quiere indicar que tomaremos el resto del scale
    "EMotor"        :   [5, 1,  -4, 0,          3600],
    "QCombustible"  :   [1, 2,  0.05, 0,        120] ,
    "Horometro"     :   [1, 4,  0.05, 0,        3600]
}
'''