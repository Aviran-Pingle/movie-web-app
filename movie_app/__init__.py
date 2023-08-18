import os

from flask import Flask
from flask_bcrypt import Bcrypt

from movie_app.datamanager import data_manager
from movie_app.users import login_manager

bcrypt = Bcrypt()
SQLITE_DB_PATH = 'data/moviweb.db'


def create_app():
    """ Configure and create a Flask app instance """
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config.update(
        {
            'SECRET_KEY': os.getenv('secret_key'),
            'SQLALCHEMY_DATABASE_URI':
                f'sqlite:///{os.path.join(basedir, SQLITE_DB_PATH)}',
        }
    )

    data_manager.db.init_app(app)
    with app.app_context():
        data_manager.db.create_all()
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from movie_app.users.views import users
    from movie_app.movies.views import movies
    from movie_app.errors.handlers import errors
    from movie_app.api.endpoints import api

    app.register_blueprint(users)
    app.register_blueprint(movies)
    app.register_blueprint(errors)
    app.register_blueprint(api, url_prefix='/api')

    return app
