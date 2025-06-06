from flask import Flask, render_template
from config import Config
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from auth import auth_bp
    from knowledge import knowledge_bp
    from rag import rag_bp
    from upload import upload_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(knowledge_bp, url_prefix='/knowledge')
    app.register_blueprint(rag_bp, url_prefix='/rag')
    app.register_blueprint(upload_bp, url_prefix='/upload')

    @app.route('/')
    def index():
        return render_template('index.html')

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
