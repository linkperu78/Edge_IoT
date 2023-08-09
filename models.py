from extensions import db

def create_model_salud_tpi(table_name):
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
            'P': self.P,
            'I': self.I,
            'F': self.F,
            }

    return MyTPIModel



def create_model_pesaje_tpi(table_name):
    # Define the model class dynamically
    class MyTPIModel(db.Model):
        __tablename__ = table_name
        Id          = db.Column(db.Integer, nullable=False ,primary_key=True)
        P           = db.Column(db.Float)
        Secuencia   = db.Column(db.String(30))
        F           = db.Column(db.String(30))
        Fecha       = db.Column(db.Integer)

        def to_dict(self):
            return {
            'P': self.P,
            'Secuencia': self.Secuencia,
            'F': self.F,
            }

    return MyTPIModel




