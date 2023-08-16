from flask_login import current_user

from movie_app import data_manager
from movie_app.datamanager.models import Movie


def check_movie_response(movie: dict) -> str:
    """
    Check an api response for errors
    :param movie: dictionary representing the requested movie
    :return: the error as a string, empty string if there is no error
    """
    if not movie:
        return 'Connection error'
    if movie['Response'] == 'False':
        return movie['Error']
    if is_exist(movie):
        return 'Movie already exist!'
    return ''


def is_exist(new_movie: dict) -> bool:
    """
    Check if the requested movie already exists in the storage
    :param new_movie: requested movie
    :return: True if the movie exist in storage, False otherwise
    """
    movie = Movie.query.filter_by(name=new_movie['Title'],
                                  user_id=current_user.id).first()
    if movie:
        return True
    return False


def create_movie_obj(movie_res: dict):
    """
    Create a movie object from the api response
    :param movie_res: movie data received from the api
    :return: dictionary representing a movie
    """
    return Movie(name=movie_res['Title'], director=movie_res['Director'],
                 year=movie_res['Year'], rating=movie_res['imdbRating'],
                 poster=movie_res['Poster'], user_id=current_user.id)
