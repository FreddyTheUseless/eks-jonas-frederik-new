from .. import db

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    teamname = db.Column(db.String(100))
    teamdescription = db.Column(db.String(100))
    teamowner = db.Column(db.Integer())