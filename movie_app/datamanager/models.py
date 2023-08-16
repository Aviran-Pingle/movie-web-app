from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    Model class representing user information.

    Attributes:
        id (int): Unique identifier for the user.
        name (str): User's name.
        email (str): User's email address (unique).
        password (str): User's hashed password.
        movies (Relationship): One-to-many relationship with Movie objects
        associated with the user.

    Inherits:
        UserMixin: Provided by Flask-Login for user authentication support.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=True, nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)


class Movie(db.Model):
    """
    Model class representing movie details.

    Attributes:
        id (int): Unique identifier for the movie.
        name (str): Movie's title.
        director (str): Director of the movie.
        year (int): Year of the movie's release.
        rating (float): Movie's rating.
        poster (str): URL to the movie's poster.
        user_id (int): Foreign key referencing the associated User.
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float)
    poster = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
