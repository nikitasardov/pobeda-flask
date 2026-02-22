from flask import Flask

from app.config import SECRET_KEY, DEBUG
from app.models import init_db
from app.routes import api


def create_app():
    app = Flask(
        __name__,
        static_folder='../static',
        static_url_path='/static'
    )
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG

    app.register_blueprint(api)

    with app.app_context():
        init_db()

    return app
