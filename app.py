from flask import Flask
from config import Config
from models import db
from auth import auth_bp
from knowledge import knowledge_bp
from rag import rag_bp
from upload import upload_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(knowledge_bp)
    app.register_blueprint(rag_bp)
    app.register_blueprint(upload_bp)
    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
