from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, logout_user, current_user

from movie_app import data_manager
from movie_app.users.forms import LoginForm, RegistrationForm
from movie_app.users.login_manager import authenticate_user
from movie_app.users.utils import create_user_obj

users = Blueprint('users', __name__)


@users.route('/', methods=['GET', 'POST'])
def login():
    """
    Render a login page (unless the user is already logged in), and handle
    the submitted login form
    """
    if current_user.is_authenticated:
        return redirect(url_for('movies.list_movies',
                                user_id=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        if authenticate_user(form.email.data, form.password.data,
                             form.remember.data):
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('movies.list_movies',
                                    user_id=current_user.id))
        else:
            flash('Login failed, check email and password', 'danger')
    return render_template('login.html', form=form)


@users.route('/login/<int:user_id>')
def specific_login(user_id):
    """
    Render a login page with prefilled email address of a requested user
    """
    if current_user.is_authenticated:
        flash('Logout if you want to switch user', 'warning')
        return redirect(url_for('users.list_users'))
    form = LoginForm()
    form.email.data = data_manager.get_user_email(user_id)
    return render_template('login.html', form=form)


@users.route('/users')
def list_users():
    """ Render list of registered users """
    all_users = data_manager.get_all_users()
    return render_template('users.html', users=all_users)


@users.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Render a registration page,handle the form submission
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = create_user_obj(form)
        data_manager.add_user(user)
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/logout')
@login_required
def logout():
    """ Handle a request to logout """
    logout_user()
    return redirect(url_for('users.login'))
