from flask_login import UserMixin, login_user

from movie_app import login_manager, data_manager, bcrypt


class User(UserMixin):
    def __init__(self, email):
        self.id = email


@login_manager.user_loader
def load_user(email: str):
    """
     Callback that is used to reload the user object from the user ID
     stored in the session
     :param email: used as the user's id
     """
    return User(email)


def authenticate_user(form_email: str, form_password: str,
                      remember: bool) -> bool:
    """
    Authenticate user login
    :param form_email: submitted email from the login form
    :param form_password: submitted password from the login form
    :param remember: "remember me" field value
    :return: True if the user is authenticated, False otherwise
    """
    user = data_manager.get_user_by_email(form_email)
    if user and bcrypt.check_password_hash(user['password'], form_password):
        login_user(User(form_email), remember=remember)
        return True
    return False
