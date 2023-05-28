from flask import Flask, jsonify
from models import Data
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dato.db'

    db.init_app(app)

    @app.route('/timeseries_data')
    def timeseries_data():
        timeseries_data = Data.query.all()
        return jsonify([d.to_dict() for d in timeseries_data])

    return app


app = create_app()

#if __name__ == '__main__':
    #app.run()