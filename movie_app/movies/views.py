from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user

import movie_app.movies.utils as movie_utils
from movie_app.datamanager import data_manager
from movie_app.movies.forms import AddMovieForm, UpdateMovieForm
from movie_app.movies.movies_data_fetcher import fetch_movie_data

movies = Blueprint('movies', __name__)


@movies.route('/users/<int:user_id>')
@login_required
def list_movies(user_id):
    """
    Render user's movie list
    :param user_id: the user's identifier
    """
    if user_id != current_user.id:
        abort(403)
    user_movies = data_manager.get_user_movies(current_user.id)
    return render_template('movies.html', movies=user_movies)


@movies.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie(user_id):
    """
    Render a form to add a new movie to the user's movie list,
    handle the form submission
    :param user_id: the user's identifier
    """
    if user_id != current_user.id:
        abort(403)
    form = AddMovieForm()
    if form.validate_on_submit():
        movie = fetch_movie_data(form.name.data)
        error = movie_utils.check_movie_response(movie)
        if error:
            flash(f'{error}', 'danger')
        else:
            movie_obj = movie_utils.create_movie_obj(movie)
            data_manager.add_movie(movie_obj)
            return redirect(url_for('movies.list_movies',
                                    user_id=current_user.id))
    return render_template('add_movie.html', form=form)


@movies.route('/users/<int:user_id>/update_movie/<int:movie_id>',
              methods=['GET', 'POST'])
@login_required
def update_movie(user_id, movie_id):
    """
    Render a form to update an existing movie from the user's movie list,
    handle the form submission
    :param user_id: the user's identifier
    :param movie_id: the movie's identifier
    """
    if user_id != current_user.id:
        abort(403)
    movie = data_manager.find_movie_by_id(movie_id)
    form = UpdateMovieForm()
    if form.validate_on_submit():
        data_manager.update_movie(movie_id, form)
        return redirect(url_for('movies.list_movies', user_id=current_user.id))

    form.name.data = movie.name
    form.rating.data = float(movie.rating)
    form.director.data = movie.director
    form.year.data = movie.year
    return render_template('update_movie.html', form=form)


@movies.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
@login_required
def delete_movie(user_id, movie_id):
    """
    Handle a request to delete a movie from a user's list
    :param user_id: the user's identifier (email)
    :param movie_id: the movie's identifier (int)
    """
    if user_id != current_user.id:
        abort(403)
    data_manager.delete_movie(movie_id)
    return redirect(url_for('movies.list_movies', user_id=current_user.id))

