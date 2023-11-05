from API.amasetia_app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'newUser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    extraversion = db.Column(db.Integer)