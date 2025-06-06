from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Knowledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)


class Chunk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    knowledge_id = db.Column(db.Integer, db.ForeignKey('knowledge.id'))
    content = db.Column(db.Text, nullable=False)
    vector = db.Column(db.PickleType)
