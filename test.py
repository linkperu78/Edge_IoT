from flask import Flask, jsonify, render_template
import models as B 
from models import mac, cargadora, id_empresa

from extensions import db
import math
import time


id_maquina = cargadora
packages_size = 300
#database_name = 'back_data.db'
database_name = 'dato.db'
#ip_default = "192.168.18.181"
ip_default =  "10.42.0.1"

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
        size = len(B.Salud.query.all())
        number_packages = math.ceil(size / packages_size)
        return f"{number_packages}"
        #return "585"

    @app.route("/salud/total")
    def total():
        size = len(B.Salud.query.all())
        return f"Tamaño de Salud = {size}"

    @app.route('/salud/datos/<int:part>')
    def specific_data(part):
        package_size = packages_size
        offset = (part - 1) * package_size
        limit = package_size
        try:
            data = B.Salud.query.offset(offset).limit(limit).all()
            original = [d.to_dict() for d in data]
            new_json = {
                "idEmpresa" : id_empresa,
                "idDispositivo" : mac,
                "Cargadora" : id_maquina,
                "registro" : original
            }

            destination_rows = []
            for row in data:
                destination_row = B.Salud_tested(P = row.P, I = row.I, F = row.F)
                destination_rows.append(destination_row)
            db.session.bulk_save_objects(destination_rows)
            db.session.commit()
            
            return (new_json)
        
        except Exception as e:
            return f"Error = {e}"
        
    

    @app.route('/test/size')
    def get_test_table_size():
        size = len(B.Salud_tested.query.all())
        number_packages = math.ceil(size / packages_size)
        return f"{number_packages}"


    @app.route('/test/<int:part>')
    def test_packages(part):
        package_size = packages_size
        offset = (part - 1) * package_size
        limit = package_size
        data = B.Salud_tested.query.offset(offset).limit(limit).all()
        original = [d.to_dict() for d in data]
        return original


    return app


app = create_app()
if __name__ == '__main__':
    #app.run(host = ip_default, port = 5000)
    app.run()
