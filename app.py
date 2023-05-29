from flask import Flask, jsonify, render_template
from models import Salud as Data
from extensions import db
import math

packages_size = 300

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dato.db'

    db.init_app(app)

    @app.route("/salud/size")
    def hello_world():
        size = len(Data.query.all())
        number_packages = math.ceil(size / packages_size)
        return f"{number_packages}"

    @app.route('/salud')
    def all_data():
        data = Data.query.all()
        return jsonify([d.to_dict() for d in data])

    @app.route('/salud/<int:part>')
    def specific_data(part):
        package_size = 300
        offset = (part - 1) * package_size
        limit = package_size

        data = Data.query.offset(offset).limit(limit).all()
        return jsonify([d.to_dict() for d in data])

    return app


app = create_app()

if __name__ == '__main__':
    app.run()