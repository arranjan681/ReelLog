from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_name = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text, nullable=True)
    poster_url = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)


class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_name = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)
