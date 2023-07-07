import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from movie_app.datamanager.json_data_manager import JSONDataManager

JSON_PATH = './movie_app/data.json'

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
data_manager = JSONDataManager(JSON_PATH)


def create_app():
    """ Create a Flask app instance """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('secret_key')
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from movie_app.users.views import users
    from movie_app.movies.views import movies
    from movie_app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(movies)
    app.register_blueprint(errors)
    login_manager.init_app(app)

    return app
