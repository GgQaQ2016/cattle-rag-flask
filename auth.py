from flask import Blueprint, request, jsonify, session, redirect, render_template
from models import db, User
from utils import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form if request.form else request.json
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Invalid input'}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'User exists'}), 400
        user = User(username=username, password_hash=hash_password(password))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form if request.form else request.json
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and verify_password(user.password_hash, password):
            session['user_id'] = user.id
            return redirect('/')
        return jsonify({'error': 'Invalid credentials'}), 400
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
