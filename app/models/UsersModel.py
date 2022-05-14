from flask_login import UserMixin
from .. import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(1000))
    role = db.Column(db.String(1000))
    firstname = db.Column(db.String(1000))
    surname = db.Column(db.String(1000))