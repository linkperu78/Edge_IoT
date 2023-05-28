from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Tabla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    columna1 = db.Column(db.String(50))
    columna2 = db.Column(db.String(50))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
