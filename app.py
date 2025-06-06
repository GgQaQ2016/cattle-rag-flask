from flask import Flask, render_template
from config import init_app
from models import db
from auth import bp as auth_bp
from knowledge import bp as knowledge_bp
from rag import bp as rag_bp
from upload import bp as upload_bp


def create_app():
    app = Flask(__name__)
    init_app(app)
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(knowledge_bp)
    app.register_blueprint(rag_bp)
    app.register_blueprint(upload_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
