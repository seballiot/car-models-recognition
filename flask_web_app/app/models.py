from app import db


class Cars(db.Model):
    __tablename__ = 'cars_table'

    id = db.Column(db.String(120), primary_key=True)
    prix = db.Column(db.Integer())
    Emission_de_CO2 = db.Column(db.Integer())
    Puissance = db.Column(db.Integer())
    consommation_urbaine = db.Column(db.Float())
    consommation_autoroute = db.Column(db.Float())
    vitesse_max = db.Column(db.Integer())
