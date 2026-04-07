from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class MovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[InputRequired()])
    genre = StringField("Genre", validators=[InputRequired()])
    rating = IntegerField("Rating (1–5)", validators=[InputRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField("Review")
    poster = StringField("Poster URL")
    submit = SubmitField("Add Movie")

class SearchForm(FlaskForm):
    search = StringField("Movie Title")
    genre = SelectField("Genre", choices=["All", "Action", "Comedy", "Drama", "Horror", "Sci-Fi"])
    submit = SubmitField("Search")
