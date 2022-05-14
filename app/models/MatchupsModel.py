from .. import db

class Matchups(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    tournament_id = db.Column(db.Integer())
    user_id1 = db.Column(db.Integer())
    user_id2 = db.Column(db.Integer())
    winner = db.Column(db.Integer())

