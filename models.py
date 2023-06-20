from extensions import db

mac = "456"
cargadora = "AE-SC-03"
id_empresa = 44

class Data(db.Model):
    __tablename__ = 'data'
    P = db.Column(db.Float, nullable=True, primary_key=True)
    I = db.Column(db.String(30), nullable=False, primary_key=True)
    F = db.Column(db.String(30), nullable=False, primary_key=True)

    def to_dict(self):
        return {
            'P': self.P,
            'I': self.I,
            'F': self.F
        }
    
class Salud(db.Model):
    __tablename__ = 'salud_table'
    Id = db.Column(db.Integer, nullable=False ,primary_key=True)
    P = db.Column(db.Float)
    I = db.Column(db.String(30))
    F = db.Column(db.String(30))

    def to_dict(self):
        return {
            'P': self.P,
            'I': self.I,
            'F': self.F
        }
