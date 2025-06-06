from flask import Flask
from config import Config

from auth import auth_bp
from knowledge import knowledge_bp
from rag import rag_bp
from upload import upload_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(knowledge_bp, url_prefix='/knowledge')
    app.register_blueprint(rag_bp, url_prefix='/rag')
    app.register_blueprint(upload_bp, url_prefix='/upload')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
