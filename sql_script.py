import sql_library as sql
import models as Model
import datetime

#init
my_host_sql = sql.sql_host()
name_db = "dato"

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
    "Secuencia" : 3,
    "Peso"      : 2.02,
    "Fecha"     : "2023-08-16 17:21:14",
}

# instance/dato.db
my_host_sql.set_name_db(name_db)

#my_host_sql.create_db()
#my_host_sql.delete_table(test_pesaje)
#my_host_sql.create_table(test_salud)
#my_host_sql.create_table(test_pesaje)

#my_host_sql.insert_data(test_pesaje, new_data_pesaje)
#my_host_sql.delete_table("Pesaje_TPI_2023_08_18")
my_host_sql.check_db()

