from flask import Blueprint, jsonify, request

import movie_app.api.utils as utils
from movie_app.datamanager import data_manager
from movie_app.movies.movies_data_fetcher import fetch_movie_data
from movie_app.movies.utils import create_movie_obj
from movie_app.users.login_manager import load_user

api = Blueprint('api', __name__)


@api.route('/users')
def get_all_users():
    """
    Retrieve a list of all users.
    :return: a list of dictionaries containing user information with keys
    'name' and 'email'
    """
    users = [{'name': user.name, 'email': user.email}
             for user in data_manager.get_all_users()]
    return jsonify(users)


@api.route('/users/<int:user_id>/movies')
def get_user_movies(user_id: int):
    """
    Retrieve movies for a specific user. Get user password in the request body.
    :param user_id: the ID of the user for whom to retrieve movies
    :return: a list of dictionaries representing movies
    """
    password = request.get_json().get('password')
    error, status_code = utils.authenticate_user(load_user(user_id), password)
    if error:
        return jsonify({'error': f'{error}'}), status_code

    movies = utils.create_movies_dicts(load_user(user_id))
    return jsonify(movies)


@api.route('/users/<int:user_id>/movies/add', methods=['POST'])
def add_movie(user_id):
    """
    Add a movie to a user's collection.
    Get user password and the movie name in the request body.
    :param user_id: the ID of the user to whom the movie will be added
    :return: a dictionary representing the added movie and an HTTP status code
    """
    password = request.get_json().get('password')
    error, status_code = utils.authenticate_user(load_user(user_id), password)
    if error:
        return jsonify({'error': f'{error}'}), status_code

    movie = fetch_movie_data(request.get_json().get('movie'))
    error, status_code = utils.check_movie_res(movie, user_id)
    if error:
        return jsonify({'error': f'{error}'}), status_code

    data_manager.add_movie(create_movie_obj(movie, user_id))
    return jsonify(utils.create_movie_dict_from_res(movie)), status_code


@api.route('/users/<int:user_id>/delete_movie/<int:movie_id>',
           methods=['DELETE'])
def delete_movie(user_id, movie_id):
    """
    Delete a movie from a user's collection.
    Get user password in the request body.
    :param user_id: the ID of the user from whom the movie will be deleted
    :param movie_id: the ID of the movie to be deleted
    :return: a dictionary representing the deleted movie and an HTTP
    status code
    """
    password = request.get_json().get('password')
    error, status_code = utils.authenticate_user(load_user(user_id), password)
    if error:
        return jsonify(({'error': f'{error}'})), status_code

    movie = data_manager.find_movie_by_id(movie_id)
    if not movie:
        return jsonify({'error': 'movie not found'}), 404

    data_manager.delete_movie(movie_id)
    return jsonify(utils.create_movie_dict_from_obj(movie)), 204
