from extensions import db

class pesaje_model(db.Model):
    __tablename__ = "pesaje"
    Id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fecha       = db.Column(db.String(30))
    Producto    = db.Column(db.String(30))
    Funcion     = db.Column(db.String(30))
    Secuencia   = db.Column(db.String(10))
    Peso        = db.Column(db.String(10))

    def get_row(self):
        return {
            'Fecha'     : self.Fecha,
            'Producto'  : self.Producto,
            'Funcion'   : self.Funcion,
            'Secuencia' : self.Secuencia,
            'Peso'      : self.Peso,
        }
    

class pesaje_backup_model(db.Model):
    __tablename__ = "pesaje_backup"
    Id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fecha_get   = db.Column(db.String(30))
    Fecha_post  = db.Column(db.String(30))
    Producto    = db.Column(db.String(30))
    Funcion     = db.Column(db.String(30))
    Secuencia   = db.Column(db.String(10))
    Peso        = db.Column(db.String(10))


class salud_model(db.Model):
    __tablename__ = "salud"
    Id      = db.Column(db.Integer, nullable=False ,primary_key=True)
    P       = db.Column(db.Float)
    I       = db.Column(db.String(30))
    F       = db.Column(db.String(30))

    def to_dict(self):
        return {
        'P': self.P,
        'I': self.I,
        'F': self.F,
        }


class salud_backup_model(db.Model):
    __tablename__ = "salud_backup"
    Id          = db.Column(db.Integer, nullable=False ,primary_key=True)
    P           = db.Column(db.Float)
    I           = db.Column(db.String(30))
    F_get       = db.Column(db.String(30))
    F_post      = db.Column(db.String(30))



