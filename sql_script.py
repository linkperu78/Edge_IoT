import sql_library as sql
import models as Model
import datetime

#init
my_host_sql = sql.sql_host()

my_new_model = Model.create_model_tpi("Test_salud")
new_data = {
    "P" : 0.0,
    "F" : "1687564928",
    "I" : "RPMDeseado",
}
epoch_time = 1687564928
timestamp_datetime = datetime.datetime.fromtimestamp(epoch_time)
new_data["Fecha"] =  timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')
print(new_data)

# instance/dato.db
my_host_sql.set_name_db("dato")
my_host_sql.insert_data(my_new_model, new_data)

my_host_sql.check_db()
