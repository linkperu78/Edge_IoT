from extensions import db

def create_model_salud(table_name):
    # Define the model class dynamically
    class MyTPIModel(db.Model):
        __tablename__ = table_name
        Id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
        P       = db.Column(db.Float)
        I       = db.Column(db.String(30))
        F       = db.Column(db.String(30))
        Fecha   = db.Column(db.Integer)

        def to_dict(self):
            return {
            'P': self.P,
            'I': self.I,
            'F': self.F,
            }

    return MyTPIModel


def create_model_salud_tpi(table_name):
    # Define the model class dynamically
    class SaludModel(db.Model):
        __tablename__ = table_name
        Id      = db.Column(db.Integer, nullable=False ,primary_key=True)
        P       = db.Column(db.Float)
        I       = db.Column(db.String(30))
        F       = db.Column(db.String(30))
        Fecha   = db.Column(db.Integer)

        def to_dict(self):
            return {
            'P': self.P,
            'I': self.I,
            'F': self.F,
            }

    return SaludModel


def create_model_pesaje(table_name):
    # Define the model class dynamically
    class PesajeTPIModel(db.Model):
        __tablename__ = table_name
        Id          = db.Column(db.Integer, nullable=False ,primary_key=True)
        Fecha       = db.Column(db.String(30))
        Producto    = db.Column(db.String(30))
        Funcion     = db.Column(db.String(30))
        Secuencia   = db.Column(db.Integer)
        Peso        = db.Column(db.Float)

        def to_dict(self):
            return {
            'Fecha'     : self.Fecha,
            'Producto'  : self.Producto,
            'Funcion'   : self.Funcion,
            'Secuencia' : self.Secuencia,
            'Peso'      : self.Peso,
            }

    return PesajeTPIModel


def create_model_pesaje_tpi(table_name):
    # Define the model class dynamically
    class PesajeModel(db.Model):
        __tablename__ = table_name
        Id          = db.Column(db.Integer, nullable=False ,primary_key=True)
        Fecha       = db.Column(db.String(30))
        Producto    = db.Column(db.String(30))
        Funcion     = db.Column(db.String(30))
        Secuencia   = db.Column(db.Integer)
        Peso        = db.Column(db.Float)

        def to_dict(self):
            return {
            'Fecha'     : self.Fecha,
            'Producto'  : self.Producto,
            'Funcion'   : self.Funcion,
            'Secuencia' : self.Secuencia,
            'Peso'      : self.Peso,
            }

    return PesajeModel




