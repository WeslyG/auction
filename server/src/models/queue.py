from app import db

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_lot = db.Column(db.Integer)
    id_buyer = db.Column(db.Integer)
    date_time = db.Column(db.DateTime)