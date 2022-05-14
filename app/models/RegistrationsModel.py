from .. import db

class Registrations(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    tournament_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())


