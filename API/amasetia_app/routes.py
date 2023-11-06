from flask import render_template, request, jsonify
from flask_login import login_user, login_required, logout_user
from API.amasetia_app.models.user import User 
from API.amasetia_app import db
from API.amasetia_app import app, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
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

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']

    username_exists = User.query.filter_by(username=username).first()
    email_exists = User.query.filter_by(email=email).first()

    if username_exists:
        return jsonify(error='Username already exists, please choose another'), 400

    if email_exists:
        return jsonify(error='An account with that email already exists, feel free to sign in'), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return jsonify(message='Signup successful'), 200