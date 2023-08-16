from movie_app import bcrypt
from movie_app.datamanager.models import User
from movie_app.users.forms import RegistrationForm


def hash_pass(password: str) -> str:
    """
    Encrypt user's password
    :param password: user's password
    :return: encrypted password
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')


def create_user_obj(form_data: RegistrationForm):
    """
    Create a new user based on the data from the registration form
    :param form_data: submitted registration form
    :return: User object
    """
    return User(name=form_data.name.data, email=form_data.email.data,
                password=hash_pass(form_data.password.data))
