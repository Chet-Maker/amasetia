from API.amasetia_app import db
from datetime import datetime

class MeyersBriggs(db.Model):
    __tablename__ = 'meyersbriggs'
    
    user_id = db.Column(db.Integer, db.ForeignKey('newuser.user_id'), primary_key=True)
    extraversion = db.Column(db.Integer, nullable=False)
    introversion = db.Column(db.Integer, nullable=False)
    sensing = db.Column(db.Integer, nullable=False)
    intuition = db.Column(db.Integer, nullable=False)
    thinking = db.Column(db.Integer, nullable=False)
    feeling = db.Column(db.Integer, nullable=False)
    judging = db.Column(db.Integer, nullable=False)
    perceiving = db.Column(db.Integer, nullable=False)
    created_dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, extraversion, introversion, sensing, intuition, thinking, feeling, judging, perceiving):
        self.user_id = user_id
        self.extraversion = extraversion
        self.introversion = introversion
        self.sensing = sensing
        self.intuition = intuition
        self.thinking = thinking
        self.feeling = feeling
        self.judging = judging
        self.perceiving = perceiving

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()