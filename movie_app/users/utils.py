from movie_app import bcrypt
from movie_app.users.forms import RegistrationForm


def hash_pass(password: str) -> str:
    """
    Encrypt user's password
    :param password: user's password
    :return: encrypted password
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')


def create_user_obj(form_data: RegistrationForm) -> dict:
    """
    Create a new user based on the data from the registration form
    :param form_data: submitted registration form
    :return: dictionary representing the registered user
    """
    return {
        form_data.email.data: {
            'name': form_data.name.data,
            'password': hash_pass(form_data.password.data),
            'movies': []
        }
    }
