from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class AddMovieForm(FlaskForm):
    """ Represent a movie addition form """
    name = StringField('Movie Name', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


class UpdateMovieForm(FlaskForm):
    """ Represents movie update form """
    name = StringField('Movie Name')
    year = IntegerField('Year Released', validators=[NumberRange(min=1900)])
    director = StringField('Director')
    rating = DecimalField('Rating', validators=[NumberRange(min=1, max=10)])
    submit = SubmitField('Update Movie')
