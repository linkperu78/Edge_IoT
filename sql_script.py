import sql_library as sql
import models as Model
import datetime

#init
my_host_sql = sql.sql_host()

test_salud  = Model.create_model_salud_tpi("salud")
test_pesaje = Model.create_model_pesaje_tpi("pesaje")
new_data = {
    "P" : 0.0,
    "F" : "1687564928",
    "I" : "RPMDeseado",
}

new_data_pesaje = {
    "Producto"  : "Mineral",
    "Funcion"   : "Agregar",
    "Secuencia" : 1,
    "Peso"      : 5.02,
    "Fecha"     : "2023-08-16 17:15:14",
}

# instance/dato.db
my_host_sql.set_name_db("dato")

#my_host_sql.delete_table(test_pesaje)
#my_host_sql.create_table(test_pesaje)
my_host_sql.insert_data(test_pesaje, new_data_pesaje)

#my_host_sql.check_db()

