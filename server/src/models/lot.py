from app import db

class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_author = db.Column(db.Integer)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    time = db.Column(db.DateTime)
