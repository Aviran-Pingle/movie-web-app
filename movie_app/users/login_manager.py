from flask_login import login_user

from movie_app import login_manager, bcrypt
from movie_app.datamanager.models import User


@login_manager.user_loader
def load_user(user_id: int):
    """
     Callback that is used to reload the user object from the user ID
     stored in the session
     :param user_id: user identifier
     """
    return User.query.get(user_id)


def authenticate_user(form_email: str, form_password: str,
                      remember: bool) -> bool:
    """
    Authenticate user login
    :param form_email: submitted email from the login form
    :param form_password: submitted password from the login form
    :param remember: "remember me" field value
    :return: True if the user is authenticated, False otherwise
    """
    user = User.query.filter_by(email=form_email).first()
    if user and bcrypt.check_password_hash(user.password, form_password):
        login_user(user, remember=remember)
        return True
    return False
