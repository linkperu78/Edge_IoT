import sql_library as sql
import models as Model
import datetime


#init
my_host_sql = sql.sql_host()
name_db = "database"

salud_enviados      = Model.salud_backup_model
salud_no_enviados   = Model.salud_model
pesaje_enviados     = Model.pesaje_backup_model
pesaje_no_enviados  = Model.pesaje_model

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

my_host_sql.set_name_db(name_db)
my_host_sql.create_db()

my_host_sql.create_table(salud_enviados)
my_host_sql.create_table(salud_no_enviados)
my_host_sql.create_table(pesaje_enviados)
my_host_sql.create_table(pesaje_no_enviados)

my_host_sql.check_db()

#my_host_sql.insert_data(test_pesaje, new_data_pesaje)
#my_host_sql.delete_table("Pesaje_TPI_2023_08_18")
#my_host_sql.delete_all_tables()
#my_host_sql.check_db()

