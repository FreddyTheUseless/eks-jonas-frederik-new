from .. import db

class teamsusers(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    team_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
