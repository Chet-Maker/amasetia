from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app.models import db, User
from app import app, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('No user by that name exists, feel free to signup')
            return redirect(url_for('signup'))

        if user.password != password:
            flash('Password is incorrect')
            return redirect(url_for('login'))

        login_user(user)  # Log in the user
        return redirect(url_for('home'))  # Redirect to the home page

    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        username_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if username_exists:
            flash('Username already exists, please choose another')
            return redirect(url_for('signup'))

        if email_exists:
            flash('An account with that email already exists, feel free to sign in')
            return redirect(url_for('login'))

        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('signup.html')
