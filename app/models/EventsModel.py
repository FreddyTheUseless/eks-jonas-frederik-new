from .. import db

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    eventname = db.Column(db.String(100))
    sponsor = db.Column(db.String(100))

