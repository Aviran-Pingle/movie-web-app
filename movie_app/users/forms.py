from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from movie_app import data_manager
from movie_app.datamanager.models import User


class RegistrationForm(FlaskForm):
    """ Representing a registration form """
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken!')


class LoginForm(FlaskForm):
    """ Representing a login form """
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
