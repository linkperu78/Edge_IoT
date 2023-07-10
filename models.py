from extensions import db
import header_values as const

class Salud_NE(db.Model):
    __tablename__ = const.name_salud_no_enviados
    Id = db.Column(db.Integer, nullable=False ,primary_key=True)
    P = db.Column(db.Float)
    I = db.Column(db.String(30))
    F = db.Column(db.String(30))

    def to_dict(self):
        return {
        'P': self.P,
        'I': self.I,
        'F': self.F,
        }


class Pesaje_NE(db.Model):
    __tablename__ = const.name_pesaje_no_enviados
    Id = db.Column(db.Integer, nullable=False ,primary_key=True)
    P = db.Column(db.Float)
    I = db.Column(db.String(30))
    F = db.Column(db.String(30))

    def to_dict(self):
        return {
        'P': self.P,
        'I': self.I,
        'F': self.F,
        }

class Salud_general(db.Model):
    __tablename__ = const.name_salud_general
    Id = db.Column(db.Integer, nullable=False ,primary_key=True)
    P = db.Column(db.Float)
    I = db.Column(db.String(30))
    F = db.Column(db.String(30))

    def to_dict(self):
        return {
        'P': self.P,
        'I': self.I,
        'F': self.F,
        }

def create_model_tpi(table_name):
    # Define the model class dynamically
    class MyTPIModel(db.Model):
        __tablename__ = table_name
        Id      = db.Column(db.Integer, nullable=False ,primary_key=True)
        P       = db.Column(db.Float)
        I       = db.Column(db.String(30))
        F       = db.Column(db.String(30))
        Fecha   = db.Column(db.Integer)

        def to_dict(self):
            return {
            'Id': self.Id,
            'P': self.P,
            'I': self.I,
            'F': self.F,
            }

    return MyTPIModel




