from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class MovieForm(FlaskForm):
    movie_name = StringField('Movie Name', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    release_year = IntegerField('Release Year', validators=[DataRequired()])
    rating = FloatField('Rating (1 to 5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Review')
    submit = SubmitField('Add Movie')


class WatchlistForm(FlaskForm):
    movie_name = StringField('Movie Name', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    release_year = IntegerField('Release Year', validators=[DataRequired()])
    submit = SubmitField('Add to Watchlist')
