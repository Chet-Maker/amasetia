from API.amasetia_app import db
from flask_login import UserMixin
import bcrypt

class User(UserMixin, db.Model):
    __tablename__ = 'newuser'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    created_dt = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_dt = db.Column(db.DateTime, nullable=False, default=db.func.now())
    email = db.Column(db.String(100), nullable=False, unique=True)

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
