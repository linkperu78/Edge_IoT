from extensions import db


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