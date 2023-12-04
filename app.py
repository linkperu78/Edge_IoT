from flask      import Flask, jsonify
from extensions import db

import logging
import models as M
import math
import time
import json_reader
import datetime

# Loading data
# Tabla Models
initial_values          = json_reader.get_json_from_file("sql_names.json")
database_name           = initial_values["name"]
salud_package_size      = int( initial_values["salud_size"] )
pesaje_package_size     = int( initial_values["pesaje_size"] )

# SQL Databases
M_salud_ne          = M.salud_model()
M_pesaje_ne         = M.pesaje_model()
M_backup_pesaje     = M.pesaje_backup_model
M_backup_salud      = M.salud_backup_model

# Maquinaria constantespi
initial_values          = json_reader.get_json_from_file("machine_values.json")
mac                     = initial_values["Dispositivo"]
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

    @app.route("/salud/total")
    def salud_size_total_url():
        size = len(M_salud_ne.query.all())
        return f"{size}"

    @app.route("/salud/size")
    def salud_size_url():
        size = len(M_salud_ne.query.all())
        number_packages = math.ceil(size / salud_package_size)
        return f"{number_packages}"
    
    @app.route('/mac/<value>')
    def set_parameter(value):
        global mac
        mac = value
        return f"Parameter set to: {mac}"

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
                data = {
                    "P"         : row.P,
                    "I"         : row.I,
                    "F_get"     : row.F,
                    "F_post"    : str(int(time.time())),
                }
                new_row = M_backup_salud(**data)
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
            return f"Error type in /salud/datos = {e}"
    return app


app = create_app()
if __name__ == '__main__':
    time.sleep(4)     # Wait until the device starts its Access Point
    # PC CST Group
    #app.run(host = "192.168.18.196", port  = 5000)
    # Jetson Nano
    app.run( host = "10.42.0.1", port = 5000 )

