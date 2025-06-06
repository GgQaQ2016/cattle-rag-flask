from flask import Blueprint, request, redirect, render_template, url_for, flash
from models import db, User
from utils import hash_password, verify_password, login_user, logout_user


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('User already exists')
        else:
            user = User(username=username, password_hash=hash_password(password))
            db.session.add(user)
            db.session.commit()
            flash('Registration successful')
            return redirect(url_for('auth.login'))
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and verify_password(user.password_hash, password):
            login_user(user.id)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
