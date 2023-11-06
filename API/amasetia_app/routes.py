from flask import render_template, request, jsonify
from flask_cors import cross_origin
from flask_login import login_user, current_user, login_required, logout_user
from API.amasetia_app.models.user import User
from API.amasetia_app.models.meyersbriggs import MeyersBriggs 
from API.amasetia_app import db
from API.amasetia_app import app, login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/api/login', methods=['POST'])
def login():
    print('login route hit')
    print('request', request.get_json())
    data = request.get_json()
    username = data['username']
    password = data['password']
    print(username, password)

    user = User.query.filter_by(username=username).first()

    if user is None:
        return {"error": "No user by that name exists, feel free to signup"}, 400

    if not user.check_password(password):
        return {"error": "Password is incorrect"}, 400

    login_user(user) 
    return {"message": "Login successful"}, 200

@app.route('/home')
@login_required
def home():
    # unsure if we'll need this route, but it's here for now
    data = {
        'message': 'Welcome to the home page!'
    }
    return jsonify(data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message='Logged out successfully')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    birth_date = data['birthDate']

    username_exists = User.query.filter_by(username=username).first()
    email_exists = User.query.filter_by(email=email).first()

    if username_exists:
        return jsonify(error='Username already exists, please choose another'), 400

    if email_exists:
        return jsonify(error='An account with that email already exists, feel free to sign in'), 400
    new_user = User(username=username, email=email, birth_date=birth_date)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return jsonify(message='Signup successful'), 200

@app.route('/api/userprofile', methods=['POST'])
@login_required
def userprofile():
    data = request.get_json()
    
    user_id = current_user.get_id()
    
    profile = MeyersBriggs.query.filter_by(user_id=user_id).first()
    if profile:
        profile.extraversion = data['extraversion']
        profile.introversion = data['introversion']
        profile.sensing = data['sensing']
        profile.intuition = data['intuition']
        profile.thinking = data['thinking']
        profile.feeling = data['feeling']
        profile.judging = data['judging']
        profile.perceiving = data['perceiving']
    else:
        profile = MeyersBriggs(
            user_id=user_id,
            extraversion=data['extraversion'],
            introversion=data['introversion'],
            sensing=data['sensing'],
            intuition=data['intuition'],
            thinking=data['thinking'],
            feeling=data['feeling'],
            judging=data['judging'],
            perceiving=data['perceiving']
        )
        db.session.add(profile)
    
    try:
        db.session.commit()
        return jsonify(message="UserProfile updated successfully"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
