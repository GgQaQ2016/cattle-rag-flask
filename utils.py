from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(pw_hash: str, password: str) -> bool:
    return check_password_hash(pw_hash, password)


def login_user(user_id: int):
    session['user_id'] = user_id


def logout_user():
    session.pop('user_id', None)


def current_user():
    return session.get('user_id')
