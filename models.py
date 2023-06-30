from extensions import db

mac = "456"
cargadora = "AE-SC-03"
id_empresa = 44

def create_model(table_name):
    # Define the model class dynamically
    class MyModel(db.Model):
        __tablename__ = table_name
        Id = db.Column(db.Integer, nullable=False ,primary_key=True)
        P = db.Column(db.Float)
        I = db.Column(db.String(30))
        F = db.Column(db.String(30))

        def to_dict(self):
            msg = f"{self.Id}\t{self.P}\t{self.I}\t{self.F}"
            return msg
        
    return MyModel

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
