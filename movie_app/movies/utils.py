from flask_login import current_user

from movie_app import data_manager
from movie_app.movies.forms import UpdateMovieForm


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
    user_movies = data_manager.get_user_movies(current_user.id)
    for movie in user_movies:
        if new_movie['Title'] == movie['name']:
            return True
    return False


def create_movie_obj(movie_res: dict) -> dict:
    """
    Create a movie object from the api response
    :param movie_res: movie data received from the api
    :return: dictionary representing a movie
    """
    return {
        'id': generate_movie_id(data_manager.get_user_movies(current_user.id)),
        'name': movie_res['Title'],
        'director': movie_res['Director'],
        'year': movie_res['Year'],
        'rating': movie_res['imdbRating'],
        'poster': movie_res['Poster']
    }


def create_updated_movie(form: UpdateMovieForm, movie_obj: dict) -> dict:
    """
    Create a movie dictionary with the updated data
    :param form: an object representing the update form
    :param movie_obj: dictionary representing the previous movie data
    :return: dictionary representing the updated movie
    """
    updated_data = {
        'year': form.year.data,
        'director': form.director.data,
        'rating': str(form.rating.data)
    }
    movie_obj.update(updated_data)
    return movie_obj


def generate_movie_id(user_movies: list[dict]) -> int:
    """
    Generate a new movie id
    :param user_movies: list of the user's movies
    :return: a unique id
    """
    return user_movies[-1]['id'] + 1 if user_movies else 1
