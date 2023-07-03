from flask      import Flask, jsonify
from extensions import db

import header_values as const
import my_sql as SQL
import models as M
import math
import time

id_empresa = const.id_empresa
mac = const.mac
id_maquina = const.cargadora
packages_size = const.package_size
ip_default =  const.ip_default
database_name = const.name_database

M_actual_salud  = SQL.actualizar_table_in_db(database_name)
M_salud_ne      = M.Salud_NE()
M_pesaje_ne     = M.Pesaje_NE()


def create_app():
    app = Flask(__name__)
    #logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_name

    db.init_app(app)

    @app.route("/localtime")
    def localtime():
        time_local = time.time()
        return f"{time_local}"

    @app.route("/salud/size")
    def hello_world():
        size = len(M_salud_ne.query.all())
        number_packages = math.ceil(size / packages_size)
        return f"{number_packages}"
        #return "585"

    @app.route("/salud/total")
    def total():
        size = len(M_salud_ne.query.all())
        return f"Tamaño de Salud = {size}"
        
    @app.route('/salud')
    def all_data():
        data = M_salud_ne.query.all()
        return jsonify([d.to_dict() for d in data])

    #@app.route('/salud/datos/<int:part>')
    @app.route('/salud/datos')
    def specific_data():
        # Si un dispositivo se conecta, otorgamos acceso a la base de datos y adicionalmente
        # seteamos la columna status como enviada, si se vuelve a solicitar, no se envia nada
        try:
            package_size = packages_size
            #offset = (part - 1) * package_size
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
            
            #print(msg_package)
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
    #app.run(host = ip_default, port = 5000)
    app.run()
