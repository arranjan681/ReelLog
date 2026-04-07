from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=30)])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class MovieForm(FlaskForm):
    movie_name = StringField("Movie Name", validators=[InputRequired()])
    genre = StringField("Genre", validators=[InputRequired()])
    release_year = StringField("Release Year", validators=[InputRequired()])
    rating = IntegerField("Rating (1–5)", validators=[InputRequired()])
    review = TextAreaField("Review")
    submit = SubmitField("Add Movie")


class WatchlistForm(FlaskForm):
    movie_name = StringField("Movie Name", validators=[InputRequired()])
    genre = StringField("Genre", validators=[InputRequired()])
    submit = SubmitField("Add to Watchlist")
