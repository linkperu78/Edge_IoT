from flask import Flask, jsonify, render_template
from models import Salud as Data
from models import mac, cargadora, id_empresa
import logging
from extensions import db
import math
import json
import time

id_maquina = "EQP"+cargadora
packages_size = 300


def create_app():
    app = Flask(__name__)
    #logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///back_data.db'

    db.init_app(app)

    @app.route("/localtime")
    def localtime():
        time_local = time.time()
        return f"{time_local}"

    @app.route("/salud/size")
    def hello_world():
        size = len(Data.query.all())
        number_packages = math.ceil(size / packages_size)
        return f"{number_packages}"

    @app.route('/salud')
    def all_data():
        data = Data.query.all()
        return jsonify([d.to_dict() for d in data])

    @app.route('/salud/datos/<int:part>')
    def specific_data(part):
        package_size = packages_size
        offset = (part - 1) * package_size
        limit = package_size
        data = Data.query.offset(offset).limit(limit).all()
        original = [d.to_dict() for d in data]
        new_json = {
            "idEmpresa" : id_empresa,
            "idDispositivo" : mac,
            "Cargadota" : id_maquina,
            "registro" : original
        }
        return (new_json)
    return app

app = create_app()
if __name__ == '__main__':
    app.run()