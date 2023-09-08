from flask      import Flask, jsonify
from extensions import db

import logging
import models as M
import math
import time
import json_reader
import sql_library as SQL
import datetime

# Loading data
# Tabla Models
initial_values = json_reader.get_json_from_file("sql_names.json")
database_name           = initial_values["name"]
salud_table_name        = initial_values["table_salud"]
pesaje_table_name       = initial_values["table_pesaje"]
salud_package_size      = int( initial_values["salud_size"] )
pesaje_package_size     = int( initial_values["pesaje_size"] )

# SQL Databases
M_salud_ne      = M.create_model_salud_tpi(salud_table_name)
M_pesaje_ne     = M.create_model_pesaje_tpi(pesaje_table_name)

_sql_ = SQL.sql_host()
_sql_.set_name_db(database_name)
M_actual_salud  = _sql_.get_today_table("Salud")

#M_actual_pesaje = _sql_.get_today_table("Pesaje")
_sql_.end_host()


# Maquinaria constantes
initial_values          = json_reader.get_json_from_file("machine_values.json")
mac                     = initial_values["MAC"]
id_maquina              = initial_values["Cargadora"]
id_empresa              = initial_values["IdEmpresa"]


def create_app():
    app = Flask(__name__)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_name + ".db"
    db.init_app(app)

    @app.route("/localtime")
    def localtime_url():
        time_local = time.time()
        time.sleep(1)
        return f"{time_local}"
    
    @app.route('/datetime')
    def datetime_url():
        epoch_time = time.time()
        my_time = datetime.datetime.fromtimestamp(epoch_time)
        my_time = my_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{my_time}"


    @app.route("/salud/size")
    def salud_size_url():
        size = len(M_salud_ne.query.all())
        number_packages = math.ceil(size / salud_package_size)
        return f"{number_packages}"
    
    @app.route("/pesaje/size")
    def pesaje_size_url():
        size = len(M_pesaje_ne.query.all())
        number_packages = math.ceil(size / salud_package_size)
        return f"{number_packages}"


    @app.route('/salud/datos')
    def salud_data_url():
        # Si un dispositivo se conecta, otorgamos acceso a la base de datos y adicionalmente
        # seteamos la columna status como enviada, si se vuelve a solicitar, no se envia nada
        try:
            package_size = salud_package_size
            limit = package_size
            data = M_salud_ne.query.limit(limit).all()
            msg_package = []
            for row in data:
                msg_package.append(row.to_dict())
                new_row = M_actual_salud()
                new_row.F, new_row.P, new_row.I  = row.F, row.P, row.I
                new_row.Fecha = int(row.F)
                db.session.add(new_row)
                db.session.delete(row)
            db.session.commit()
            new_json = {
                "idEmpresa" : id_empresa,
                "idDispositivo" : mac,
                "Cargadora" : id_maquina,
                "registro" : msg_package
            }
            return (new_json)
        except Exception as e:
            return f"Error type = {e}"
        


    @app.route('/pesaje/datos')
    def pesaje_data_url():
        # Si un dispositivo se conecta, otorgamos acceso a la base de datos y adicionalmente
        # seteamos la columna status como enviada, si se vuelve a solicitar, no se envia nada
        try:
            package_size = pesaje_package_size
            limit = package_size
            data = M_pesaje_ne.query.limit(limit).all()
            msg_package = []

            for row in data:
                my_row_dictionary = row.to_dict()
                new_pesaje_row = M_actual_pesaje(**my_row_dictionary)
                my_row_dictionary['Cargadora']  = '777'
                my_row_dictionary['Actividad']  = "Limpieza"
                my_row_dictionary['Camion']     = "V3"
                my_row_dictionary['Origen']     = "Tajo1"
                msg_package.append(my_row_dictionary)
                db.session.add(new_pesaje_row)
            db.session.commit()
            new_json = {
                "idEmpresa" : id_empresa,
                "idDispositivo" : mac,
                "Cargadora" : id_maquina,
                "registro" : msg_package
            }
            return (new_json)
        except Exception as e:
            return f"Error type = {e}"
        
    return app


app = create_app()
if __name__ == '__main__':
    app.run( host = "10.42.0.1", port = 5000 )
    #app.run( host = "10.42.0.1")
