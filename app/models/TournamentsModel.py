from .. import db

class Tournaments(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    event_id = db.Column(db.Integer())
    tournamentname = db.Column(db.String(100))
    venue = db.Column(db.String(100))
    game = db.Column(db.String(100))
    size = db.Column(db.Integer())