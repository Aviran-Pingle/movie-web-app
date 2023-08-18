from movie_app import bcrypt
from movie_app.datamanager.models import Movie, User


def authenticate_user(user: User, password: str) -> tuple:
    """
    Authenticate a user with their password.
    :param user: the user object to authenticate
    :param password: the provided password for authentication
    :return: a tuple containing a message and HTTP status code
    """
    if not user:
        return 'user not found', 404
    if not password:
        return 'missing password', 400
    if not bcrypt.check_password_hash(user.password, password):
        return 'wrong password', 401
    return '', 200


def create_movies_dicts(user: User) -> list:
    """
    Create a list of dictionaries representing the user's movies.
    :param user: the user object for which to create movies dictionaries
    :return: a list of dictionaries, each representing a movie
    """
    return [
        {
            'name': movie.name,
            'director': movie.director,
            'year': movie.director,
            'rating': movie.rating,
            'poster': movie.poster
        }
        for movie in user.movies
    ]


def create_movie_dict_from_res(movie_res: dict) -> dict:
    """
    Create a dictionary representing a movie from an API response.

    :param movie_res: the movie data received from an API response
    :return: a dictionary containing movie details
    """
    return {
        'name': movie_res['Title'],
        'director': movie_res['Director'],
        'year': movie_res['Year'],
        'rating': movie_res['imdbRating'],
        'poster': movie_res['Poster']
    }


def create_movie_dict_from_obj(movie_obj: Movie) -> dict:
    """
     Create a dictionary representing a movie from a Movie object.
    :param movie_obj: the Movie object from which to create a dictionary
    :return: a dict containing movie details
    """
    return {
        'name': movie_obj.name,
        'director':  movie_obj.director,
        'year':  movie_obj.year,
        'rating':  movie_obj.rating,
        'poster':  movie_obj.poster
    }


def check_movie_res(movie: dict, user_id: int) -> tuple:
    """
    Check the validity of a movie response and its existence for a user.
    :param movie: the movie data received from an API response
    :param user_id: the ID of the user associated with the movie
    :return: a tuple containing a message and HTTP status code
    """
    if not movie:
        return 'Connection error', 500
    if movie['Response'] == 'False':
        return movie['Error'], 404
    if Movie.query.filter_by(name=movie['Title'], user_id=user_id).first():
        return 'Movie already exist!', 400
    return '', 201
