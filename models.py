from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class Knowledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("knowledges", lazy=True))


class Chunk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    embedding = db.Column(db.PickleType)
    knowledge_id = db.Column(db.Integer, db.ForeignKey("knowledge.id"))
    knowledge = db.relationship(
        "Knowledge", backref=db.backref("chunks", lazy=True)
    )
